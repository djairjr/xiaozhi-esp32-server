const SAMPLE_RATE = 16000;
const CHANNELS = 1;
const FRAME_SIZE = 960;  // corresponds_to_60ms_frame_size (16000Hz * 0.06s = 960 samples)
const OPUS_APPLICATION = 2049; // OPUS_APPLICATION_AUDIO
const BUFFER_SIZE = 4096;

let audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: SAMPLE_RATE });
let mediaStream, mediaSource, audioProcessor;
let recordedPcmData = []; // store_raw_pcm_data
let recordedOpusData = []; // store_opus_encoded_data
let opusEncoder, opusDecoder;
let isRecording = false;

const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const playButton = document.getElementById("play");
const statusLabel = document.getElementById("status");

startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
playButton.addEventListener("click", playRecording);

// initialize_opus_encoder_and_decoder
async function initOpus() {
    if (typeof window.ModuleInstance === 'undefined') {
        if (typeof Module !== 'undefined') {
            // try_using_globalmodule
            window.ModuleInstance = Module;
            console.log('使用全局Module作为ModuleInstance');
        } else {
            console.error("Opus library not loaded, neither ModuleInstance nor Module object exists");
            return false;
        }
    }
    
    try {
        const mod = window.ModuleInstance;
        
        // create_an_encoder
        opusEncoder = {
            channels: CHANNELS,
            sampleRate: SAMPLE_RATE,
            frameSize: FRAME_SIZE,
            maxPacketSize: 4000,
            module: mod,
            
            // initialize_the_encoder
            init: function() {
                // get_encoder_size
                const encoderSize = mod._opus_encoder_get_size(this.channels);
                console.log(`Opus编码器大小: ${encoderSize}byte`);
                
                // allocate_memory
                this.encoderPtr = mod._malloc(encoderSize);
                if (!this.encoderPtr) {
                    throw new Error("Unable to allocate encoder memory");
                }
                
                // initialize_the_encoder
                const err = mod._opus_encoder_init(
                    this.encoderPtr,
                    this.sampleRate,
                    this.channels,
                    OPUS_APPLICATION
                );
                
                if (err < 0) {
                    throw new Error(`Opus编码器初始化失败: ${err}`);
                }
                
                return true;
            },
            
            // coding_method
            encode: function(pcmData) {
                const mod = this.module;
                
                // allocate_memory_for_pcm_data
                const pcmPtr = mod._malloc(pcmData.length * 2); // Int16 = 2 bytes
                
                // copy_data_to_wasm_memory
                for (let i = 0; i < pcmData.length; i++) {
                    mod.HEAP16[(pcmPtr >> 1) + i] = pcmData[i];
                }
                
                // allocate_memory_for_opus_encoded_data
                const maxEncodedSize = this.maxPacketSize;
                const encodedPtr = mod._malloc(maxEncodedSize);
                
                // coding
                const encodedBytes = mod._opus_encode(
                    this.encoderPtr,
                    pcmPtr,
                    this.frameSize,
                    encodedPtr,
                    maxEncodedSize
                );
                
                if (encodedBytes < 0) {
                    mod._free(pcmPtr);
                    mod._free(encodedPtr);
                    throw new Error(`Opus编码失败: ${encodedBytes}`);
                }
                
                // copy_the_encoded_data
                const encodedData = new Uint8Array(encodedBytes);
                for (let i = 0; i < encodedBytes; i++) {
                    encodedData[i] = mod.HEAPU8[encodedPtr + i];
                }
                
                // free_memory
                mod._free(pcmPtr);
                mod._free(encodedPtr);
                
                return encodedData;
            },
            
            // destruction_method
            destroy: function() {
                if (this.encoderPtr) {
                    this.module._free(this.encoderPtr);
                    this.encoderPtr = null;
                }
            }
        };
        
        // create_decoder
        opusDecoder = {
            channels: CHANNELS,
            rate: SAMPLE_RATE,
            frameSize: FRAME_SIZE,
            module: mod,
            
            // initialize_decoder
            init: function() {
                // get_decoder_size
                const decoderSize = mod._opus_decoder_get_size(this.channels);
                console.log(`Opus解码器大小: ${decoderSize}byte`);
                
                // allocate_memory
                this.decoderPtr = mod._malloc(decoderSize);
                if (!this.decoderPtr) {
                    throw new Error("Unable to allocate decoder memory");
                }
                
                // initialize_decoder
                const err = mod._opus_decoder_init(
                    this.decoderPtr,
                    this.rate,
                    this.channels
                );
                
                if (err < 0) {
                    throw new Error(`Opus解码器初始化失败: ${err}`);
                }
                
                return true;
            },
            
            // decoding_method
            decode: function(opusData) {
                const mod = this.module;
                
                // allocate_memory_for_opus_data
                const opusPtr = mod._malloc(opusData.length);
                mod.HEAPU8.set(opusData, opusPtr);
                
                // allocate_memory_for_pcm_output
                const pcmPtr = mod._malloc(this.frameSize * 2); // Int16 = 2 bytes
                
                // decoding
                const decodedSamples = mod._opus_decode(
                    this.decoderPtr,
                    opusPtr,
                    opusData.length,
                    pcmPtr,
                    this.frameSize,
                    0 // not_using_fec
                );
                
                if (decodedSamples < 0) {
                    mod._free(opusPtr);
                    mod._free(pcmPtr);
                    throw new Error(`Opus解码失败: ${decodedSamples}`);
                }
                
                // copy_decoded_data
                const decodedData = new Int16Array(decodedSamples);
                for (let i = 0; i < decodedSamples; i++) {
                    decodedData[i] = mod.HEAP16[(pcmPtr >> 1) + i];
                }
                
                // free_memory
                mod._free(opusPtr);
                mod._free(pcmPtr);
                
                return decodedData;
            },
            
            // destruction_method
            destroy: function() {
                if (this.decoderPtr) {
                    this.module._free(this.decoderPtr);
                    this.decoderPtr = null;
                }
            }
        };
        
        // initialize_encoder_and_decoder
        if (opusEncoder.init() && opusDecoder.init()) {
            console.log("Opus encoder and decoder initialized successfully.");
            return true;
        } else {
            console.error("Opus initialization failed");
            return false;
        }
    } catch (error) {
        console.error("Opus initialization failed:", error);
        return false;
    }
}

// convert_float32_audio_data_to_int16_audio_data
function convertFloat32ToInt16(float32Data) {
    const int16Data = new Int16Array(float32Data.length);
    for (let i = 0; i < float32Data.length; i++) {
        // will[-1,1]the_range_is_converted_to[-32768,32767]
        const s = Math.max(-1, Math.min(1, float32Data[i]));
        int16Data[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    return int16Data;
}

// convert_int16_audio_data_to_float32_audio_data
function convertInt16ToFloat32(int16Data) {
    const float32Data = new Float32Array(int16Data.length);
    for (let i = 0; i < int16Data.length; i++) {
        // will[-32768,32767]the_range_is_converted_to[-1,1]
        float32Data[i] = int16Data[i] / (int16Data[i] < 0 ? 0x8000 : 0x7FFF);
    }
    return float32Data;
}

function startRecording() {
    if (isRecording) return;
    
    // make_sure_you_have_permissions_and_the_audiocontext_is_active
    if (audioContext.state === 'suspended') {
        audioContext.resume().then(() => {
            console.log("AudioContext has been restored");
            continueStartRecording();
        }).catch(err => {
            console.error("Failed to restore AudioContext:", err);
            statusLabel.textContent = "Unable to activate audio context, please click again";
        });
    } else {
        continueStartRecording();
    }
}

// the_logic_to_actually_start_recording
function continueStartRecording() {
    // reset_recording_data
    recordedPcmData = [];
    recordedOpusData = [];
    window.audioDataBuffer = new Int16Array(0); // reset_buffer
    
    // initialize_opus
    initOpus().then(success => {
        if (!success) {
            statusLabel.textContent = "Opus initialization failed";
            return;
        }
        
        console.log("Start recording, parameters:", {
            sampleRate: SAMPLE_RATE,
            channels: CHANNELS,
            frameSize: FRAME_SIZE,
            bufferSize: BUFFER_SIZE
        });
        
        // request_microphone_permission
        navigator.mediaDevices.getUserMedia({ 
            audio: {
                sampleRate: SAMPLE_RATE,
                channelCount: CHANNELS,
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            } 
        })
        .then(stream => {
            console.log("Get the microphone stream, actual parameters:", stream.getAudioTracks()[0].getSettings());
            
            // check_if_the_stream_is_valid
            if (!stream || !stream.getAudioTracks().length || !stream.getAudioTracks()[0].enabled) {
                throw new Error("The audio stream obtained is invalid");
            }
            
            mediaStream = stream;
            mediaSource = audioContext.createMediaStreamSource(stream);
            
            // create_scriptprocessor(although_deprecated，but_good_compatibility)
            // try_using_audioworklet_before_downgrading_to_scriptprocessor
            createAudioProcessor().then(processor => {
                if (processor) {
                    console.log("Use AudioWorklet to process audio");
                    audioProcessor = processor;
                    // connect_the_audio_processing_chain
                    mediaSource.connect(audioProcessor);
                    audioProcessor.connect(audioContext.destination);
                } else {
                    console.log("Fallback to ScriptProcessor");
                    // create_scriptprocessor_node
                    audioProcessor = audioContext.createScriptProcessor(BUFFER_SIZE, CHANNELS, CHANNELS);
                    
                    // process_audio_data
                    audioProcessor.onaudioprocess = processAudioData;
                    
                    // connect_the_audio_processing_chain
                    mediaSource.connect(audioProcessor);
                    audioProcessor.connect(audioContext.destination);
                }
                
                // update_ui
                isRecording = true;
                statusLabel.textContent = "Recording...";
                startButton.disabled = true;
                stopButton.disabled = false;
                playButton.disabled = true;
            }).catch(error => {
                console.error("Failed to create audio processor:", error);
                statusLabel.textContent = "Failed to create audio processor";
            });
        })
        .catch(error => {
            console.error("Failed to get microphone:", error);
            statusLabel.textContent = "Failed to get microphone:" + error.message;
        });
    });
}

// create_audioworklet_processor
async function createAudioProcessor() {
    try {
        // try_using_the_more_modern_audioworklet API
        if ('AudioWorklet' in window && 'AudioWorkletNode' in window) {
            // define_audioworklet_processor_code
            const workletCode = `
                class OpusRecorderProcessor extends AudioWorkletProcessor {
                    constructor() {
                        super();
                        this.buffers = [];
                        this.frameSize = ${FRAME_SIZE};
                        this.buffer = new Float32Array(this.frameSize);
                        this.bufferIndex = 0;
                        this.isRecording = false;
                        
                        this.port.onmessage = (event) => {
                            if (event.data.command === 'start') {
                                this.isRecording = true;
                            } else if (event.data.command === 'stop') {
                                this.isRecording = false;
                                // send_last_buffer
                                if (this.bufferIndex > 0) {
                                    const finalBuffer = this.buffer.slice(0, this.bufferIndex);
                                    this.port.postMessage({ buffer: finalBuffer });
                                }
                            }
                        };
                    }
                    
                    process(inputs, outputs) {
                        if (!this.isRecording) return true;
                        
                        // get_input_data
                        const input = inputs[0][0]; // mono channel
                        if (!input || input.length === 0) return true;
                        
                        // add_input_data_to_buffer
                        for (let i = 0; i < input.length; i++) {
                            this.buffer[this.bufferIndex++] = input[i];
                            
                            // when_buffer_fills_up，send_to_main_thread
                            if (this.bufferIndex >= this.frameSize) {
                                this.port.postMessage({ buffer: this.buffer.slice() });
                                this.bufferIndex = 0;
                            }
                        }
                        
                        return true;
                    }
                }
                
                registerProcessor('opus-recorder-processor', OpusRecorderProcessor);
            `;
            
            // create_blob URL
            const blob = new Blob([workletCode], { type: 'application/javascript' });
            const url = URL.createObjectURL(blob);
            
            // load_audioworklet_module
            await audioContext.audioWorklet.addModule(url);
            
            // create_audioworkletnode
            const workletNode = new AudioWorkletNode(audioContext, 'opus-recorder-processor');
            
            // handle_messages_received_from_audioworklet
            workletNode.port.onmessage = (event) => {
                if (event.data.buffer) {
                    // use_the_same_processing_logic_as_scriptprocessor
                    processAudioData({
                        inputBuffer: {
                            getChannelData: () => event.data.buffer
                        }
                    });
                }
            };
            
            // start_recording
            workletNode.port.postMessage({ command: 'start' });
            
            // save_stop_function
            workletNode.stopRecording = () => {
                workletNode.port.postMessage({ command: 'stop' });
            };
            
            console.log("AudioWorklet audio processor created successfully");
            return workletNode;
        }
    } catch (error) {
        console.error("Failed to create AudioWorklet, ScriptProcessor will be used:", error);
    }
    
    // if_audioworklet_is_unavailable_or_fails，return_null_to_fallback_to_scriptprocessor
    return null;
}

// process_audio_data
function processAudioData(e) {
    // get_input_buffer
    const inputBuffer = e.inputBuffer;
    
    // get_the_float32_data_of_the_first_channel
    const inputData = inputBuffer.getChannelData(0);
    
    // add_debugging_information
    const nonZeroCount = Array.from(inputData).filter(x => Math.abs(x) > 0.001).length;
    console.log(`audio_data_received: ${inputData.length} samples, number_of_nonzero_samples: ${nonZeroCount}`);
    
    // if_all_are_0，maybe_the_microphone_isnt_picking_up_the_sound_correctly
    if (nonZeroCount < 5) {
        console.warn("Warning: large_number_of_silent_samples_detected, please check if the microphone is working properly");
        // continue_processing，just_in_case_some_samples_are_indeed_muted
    }
    
    // store_pcm_data_for_debugging
    recordedPcmData.push(new Float32Array(inputData));
    
    // convert_to_int16_data_for_opus_encoding
    const int16Data = convertFloat32ToInt16(inputData);
    
    // if_the_collected_data_is_not_an_integer_multiple_of_frame_size，need_to_be_processed
    // create_a_static_buffer_to_store_less_than_one_frame_of_data
    if (!window.audioDataBuffer) {
        window.audioDataBuffer = new Int16Array(0);
    }
    
    // merge_previously_cached_data_with_new_data
    const combinedData = new Int16Array(window.audioDataBuffer.length + int16Data.length);
    combinedData.set(window.audioDataBuffer);
    combinedData.set(int16Data, window.audioDataBuffer.length);
    
    // process_full_frames
    const frameCount = Math.floor(combinedData.length / FRAME_SIZE);
    console.log(`number_of_complete_frames_that_can_be_encoded: ${frameCount}, total_buffer_size: ${combinedData.length}`);
    
    for (let i = 0; i < frameCount; i++) {
        const frameData = combinedData.subarray(i * FRAME_SIZE, (i + 1) * FRAME_SIZE);
        
        try {
            console.log(`coding_no ${i+1}/${frameCount} frame, frame_size: ${frameData.length}`);
            const encodedData = opusEncoder.encode(frameData);
            if (encodedData) {
                console.log(`encoding_successful: ${encodedData.length} byte`);
                recordedOpusData.push(encodedData);
            }
        } catch (error) {
            console.error(`Opus编码帧 ${i+1} fail:`, error);
        }
    }
    
    // save_data_remaining_for_less_than_one_frame
    const remainingSamples = combinedData.length % FRAME_SIZE;
    if (remainingSamples > 0) {
        window.audioDataBuffer = combinedData.subarray(frameCount * FRAME_SIZE);
        console.log(`reserve ${remainingSamples} samples_to_the_next_processing`);
    } else {
        window.audioDataBuffer = new Int16Array(0);
    }
}

function stopRecording() {
    if (!isRecording) return;
    
    // process_remaining_buffered_data
    if (window.audioDataBuffer && window.audioDataBuffer.length > 0) {
        console.log(`stop_recording，dispose_of_remaining ${window.audioDataBuffer.length} samples`);
        // if_the_remaining_data_is_less_than_one_frame，one_frame_can_be_made_up_by_padding_zeros
        if (window.audioDataBuffer.length < FRAME_SIZE) {
            const paddedFrame = new Int16Array(FRAME_SIZE);
            paddedFrame.set(window.audioDataBuffer);
            // the_remaining_part_is_filled_with_0
            for (let i = window.audioDataBuffer.length; i < FRAME_SIZE; i++) {
                paddedFrame[i] = 0;
            }
            try {
                console.log(`encode_last_frame(zero_padding): ${paddedFrame.length} sample`);
                const encodedData = opusEncoder.encode(paddedFrame);
                if (encodedData) {
                    recordedOpusData.push(encodedData);
                }
            } catch (error) {
                console.error("The last frame Opus encoding failed:", error);
            }
        } else {
            // if_the_data_exceeds_one_frame，follow_normal_procedures
            processAudioData({
                inputBuffer: {
                    getChannelData: () => convertInt16ToFloat32(window.audioDataBuffer)
                }
            });
        }
        window.audioDataBuffer = null;
    }
    
    // if_you_are_using_audioworklet，call_its_specific_stop_method
    if (audioProcessor && typeof audioProcessor.stopRecording === 'function') {
        audioProcessor.stopRecording();
    }
    
    // stop_microphone
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
    }
    
    // break_the_audio_processing_chain
    if (audioProcessor) {
        try {
            audioProcessor.disconnect();
            if (mediaSource) mediaSource.disconnect();
        } catch (error) {
            console.warn("Error while breaking audio processing chain:", error);
        }
    }
    
    // update_ui
    isRecording = false;
    statusLabel.textContent = "Recording has stopped, collected" + recordedOpusData.length + "Frame Opus data";
    startButton.disabled = false;
    stopButton.disabled = true;
    playButton.disabled = recordedOpusData.length === 0;
    
    console.log("Recording completed:", 
                "PCM frame number:", recordedPcmData.length, 
                "Opus frame rate:", recordedOpusData.length);
}

function playRecording() {
    if (!recordedOpusData.length) {
        statusLabel.textContent = "No recordings available to play";
        return;
    }
    
    // decode_all_opus_data_to_pcm
    let allDecodedData = [];
    
    for (const opusData of recordedOpusData) {
        try {
            // decoded_to_int16_data
            const decodedData = opusDecoder.decode(opusData);
            
            if (decodedData && decodedData.length > 0) {
                // convert_int16_data_to_float32
                const float32Data = convertInt16ToFloat32(decodedData);
                
                // added_to_total_decoded_data
                allDecodedData.push(...float32Data);
            }
        } catch (error) {
            console.error("Opus decoding failed:", error);
        }
    }
    
    // if_no_data_is_decoded，return
    if (allDecodedData.length === 0) {
        statusLabel.textContent = "Decoding failed and cannot be played";
        return;
    }
    
    // create_audio_buffer
    const audioBuffer = audioContext.createBuffer(CHANNELS, allDecodedData.length, SAMPLE_RATE);
    audioBuffer.copyToChannel(new Float32Array(allDecodedData), 0);
    
    // create_an_audio_source_and_play_it
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
    
    // update_ui
    statusLabel.textContent = "Now playing...";
    playButton.disabled = true;
    
    // restore_ui_after_playback_ends
    source.onended = () => {
        statusLabel.textContent = "Finished playing";
        playButton.disabled = false;
    };
}

// simulate_the_opus_data_returned_by_the_server_for_decoding_and_playback
function playOpusFromServer(opusData) {
    // this_function_shows_how_to_process_the_opus_data_returned_by_the_server
    // opusData should be an array containing opus frames
    
    if (!opusDecoder) {
        initOpus().then(success => {
            if (success) {
                decodeAndPlayOpusData(opusData);
            } else {
                statusLabel.textContent = "Opus decoder initialization failed";
            }
        });
    } else {
        decodeAndPlayOpusData(opusData);
    }
}

function decodeAndPlayOpusData(opusData) {
    let allDecodedData = [];
    
    for (const frame of opusData) {
        try {
            const decodedData = opusDecoder.decode(frame);
            if (decodedData && decodedData.length > 0) {
                const float32Data = convertInt16ToFloat32(decodedData);
                allDecodedData.push(...float32Data);
            }
        } catch (error) {
            console.error("Server-side Opus data decoding failed:", error);
        }
    }
    
    if (allDecodedData.length === 0) {
        statusLabel.textContent = "Server data decoding failed";
        return;
    }
    
    const audioBuffer = audioContext.createBuffer(CHANNELS, allDecodedData.length, SAMPLE_RATE);
    audioBuffer.copyToChannel(new Float32Array(allDecodedData), 0);
    
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start();
    
    statusLabel.textContent = "Playing server data...";
    source.onended = () => statusLabel.textContent = "Server data playback completed";
}
