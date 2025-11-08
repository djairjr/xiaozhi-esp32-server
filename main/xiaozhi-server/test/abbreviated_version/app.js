const SAMPLE_RATE = 16000;
const CHANNELS = 1;
const FRAME_SIZE = 960;  // corresponds_to_60ms_frame_size (16000Hz * 0.06s = 960 samples)
const OPUS_APPLICATION = 2049; // OPUS_APPLICATION_AUDIO
const BUFFER_SIZE = 4096;

// WebSocket related variables
let websocket = null;
let isConnected = false;

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

// add_websocket_interface_element_reference
const connectButton = document.getElementById("connectButton") || document.createElement("button");
const serverUrlInput = document.getElementById("serverUrl") || document.createElement("input");
const connectionStatus = document.getElementById("connectionStatus") || document.createElement("span");
const sendTextButton = document.getElementById("sendTextButton") || document.createElement("button");
const messageInput = document.getElementById("messageInput") || document.createElement("input");
const conversationDiv = document.getElementById("conversation") || document.createElement("div");

// add_connection_and_send_event_listening
if(connectButton.id === "connectButton") {
    connectButton.addEventListener("click", connectToServer);
}
if(sendTextButton.id === "sendTextButton") {
    sendTextButton.addEventListener("click", sendTextMessage);
}

startButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
playButton.addEventListener("click", playRecording);

// audio_buffering_and_playback_management
let audioBufferQueue = [];     // store_received_audio_packets
let isAudioBuffering = false;  // whether_audio_is_buffering
let isAudioPlaying = false;    // whether_audio_is_playing
const BUFFER_THRESHOLD = 3;    // buffered_packet_number_threshold，accumulate_at_least_5_packages_before_starting_playback
const MIN_AUDIO_DURATION = 0.1; // minimum_audio_length(second)，audio_shorter_than_this_length_will_be_merged
let streamingContext = null;   // audio_stream_context

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
        
        // if_websocket_is_connected，send_a_start_recording_signal
        if (isConnected && websocket && websocket.readyState === WebSocket.OPEN) {
            sendVoiceControlMessage('start');
        }
        
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
                
                // if_websocket_is_connected，send_encoded_data
                if (isConnected && websocket && websocket.readyState === WebSocket.OPEN) {
                    sendOpusDataToServer(encodedData);
                }
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
                    
                    // if_websocket_is_connected，send_last_frame
                    if (isConnected && websocket && websocket.readyState === WebSocket.OPEN) {
                        sendOpusDataToServer(encodedData);
                    }
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
    
    // if_websocket_is_connected，send_a_stop_recording_signal
    if (isConnected && websocket && websocket.readyState === WebSocket.OPEN) {
        // send_an_empty_frame_as_an_end_marker
        const emptyFrame = new Uint8Array(0);
        websocket.send(emptyFrame);
        
        // send_stop_recording_control_message
        sendVoiceControlMessage('stop');
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

// handles_modified_versions_of_binary_messages
async function handleBinaryMessage(data) {
    try {
        let arrayBuffer;

        // process_according_to_data_type
        if (data instanceof ArrayBuffer) {
            arrayBuffer = data;
            console.log(`arraybuffer_audio_data_received，size: ${data.byteLength}byte`);
        } else if (data instanceof Blob) {
            // if_it_is_a_blob_type，convert_to_arraybuffer
            arrayBuffer = await data.arrayBuffer();
            console.log(`blob_audio_data_received，size: ${arrayBuffer.byteLength}byte`);
        } else {
            console.warn(`received_binary_data_of_unknown_type: ${typeof data}`);
            return;
        }

        // create_uint8array_for_processing
        const opusData = new Uint8Array(arrayBuffer);

        if (opusData.length > 0) {
            // add_data_to_buffer_queue
            audioBufferQueue.push(opusData);
            
            // if_the_first_audio_packet_is_received，start_buffering_process
            if (audioBufferQueue.length === 1 && !isAudioBuffering && !isAudioPlaying) {
                startAudioBuffering();
            }
        } else {
            console.warn('收到空音频数据帧，可能是结束标志');
            
            // if_there_is_data_in_the_buffer_queue_and_it_is_not_playing，start_playing_now
            if (audioBufferQueue.length > 0 && !isAudioPlaying) {
                playBufferedAudio();
            }
            
            // if_playing，send_end_signal
            if (isAudioPlaying && streamingContext) {
                streamingContext.endOfStream = true;
            }
        }
    } catch (error) {
        console.error(`error_processing_binary_message:`, error);
    }
}

// start_audio_buffering_process
function startAudioBuffering() {
    if (isAudioBuffering || isAudioPlaying) return;
    
    isAudioBuffering = true;
    console.log("Start audio buffering...");
    
    // set_timeout，if_not_enough_audio_packets_are_collected_within_a_certain_period_of_time，just_start_playing
    setTimeout(() => {
        if (isAudioBuffering && audioBufferQueue.length > 0) {
            console.log(`buffer_timeout，current_number_of_buffered_packets: ${audioBufferQueue.length}，start_playing`);
            playBufferedAudio();
        }
    }, 300); // 300ms timeout
    
    // monitor_buffering_progress
    const bufferCheckInterval = setInterval(() => {
        if (!isAudioBuffering) {
            clearInterval(bufferCheckInterval);
            return;
        }
        
        // when_enough_audio_packets_have_been_accumulated，start_playing
        if (audioBufferQueue.length >= BUFFER_THRESHOLD) {
            clearInterval(bufferCheckInterval);
            console.log(`buffered ${audioBufferQueue.length} audio_package，start_playing`);
            playBufferedAudio();
        }
    }, 50);
}

// play_buffered_audio
function playBufferedAudio() {
    if (isAudioPlaying || audioBufferQueue.length === 0) return;
    
    isAudioPlaying = true;
    isAudioBuffering = false;
    
    // create_a_streaming_context
    if (!streamingContext) {
        streamingContext = {
            queue: [],          // decoded_pcm_queue
            playing: false,     // is_playing
            endOfStream: false, // whether_the_end_signal_is_received
            source: null,       // current_audio_source
            totalSamples: 0,    // the_total_number_of_samples_accumulated
            lastPlayTime: 0,    // last_played_timestamp
            // decode_opus_data_to_pcm
            decodeOpusFrames: async function(opusFrames) {
                let decodedSamples = [];
                
                for (const frame of opusFrames) {
                    try {
                        // decode_using_opus_decoder
                        const frameData = opusDecoder.decode(frame);
                        if (frameData && frameData.length > 0) {
                            // convert_to_float32
                            const floatData = convertInt16ToFloat32(frameData);
                            decodedSamples.push(...floatData);
                        }
                    } catch (error) {
                        console.error("Opus decoding failed:", error);
                    }
                }
                
                if (decodedSamples.length > 0) {
                    // add_to_decoding_queue
                    this.queue.push(...decodedSamples);
                    this.totalSamples += decodedSamples.length;
                    
                    // if_at_least_0_is_accumulated.2 seconds of audio, start_playing
                    const minSamples = SAMPLE_RATE * MIN_AUDIO_DURATION;
                    if (!this.playing && this.queue.length >= minSamples) {
                        this.startPlaying();
                    }
                }
            },
            // start_playing_audio
            startPlaying: function() {
                if (this.playing || this.queue.length === 0) return;
                
                this.playing = true;
                
                // create_new_audio_buffer
                const minPlaySamples = Math.min(this.queue.length, SAMPLE_RATE); // play_up_to_1_second
                const currentSamples = this.queue.splice(0, minPlaySamples);
                
                const audioBuffer = audioContext.createBuffer(CHANNELS, currentSamples.length, SAMPLE_RATE);
                audioBuffer.copyToChannel(new Float32Array(currentSamples), 0);
                
                // create_audio_source
                this.source = audioContext.createBufferSource();
                this.source.buffer = audioBuffer;
                
                // create_gain_nodes_for_smooth_transitions
                const gainNode = audioContext.createGain();
                
                // apply_fade_effects_to_avoid_popping_sounds
                const fadeDuration = 0.02; // 20 milliseconds
                gainNode.gain.setValueAtTime(0, audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(1, audioContext.currentTime + fadeDuration);
                
                const duration = audioBuffer.duration;
                if (duration > fadeDuration * 2) {
                    gainNode.gain.setValueAtTime(1, audioContext.currentTime + duration - fadeDuration);
                    gainNode.gain.linearRampToValueAtTime(0, audioContext.currentTime + duration);
                }
                
                // connect_the_node_and_start_playing
                this.source.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                this.lastPlayTime = audioContext.currentTime;
                console.log(`start_playing ${currentSamples.length} samples，about ${(currentSamples.length / SAMPLE_RATE).toFixed(2)} second`);
                
                // processing_after_playback_ends
                this.source.onended = () => {
                    this.source = null;
                    this.playing = false;
                    
                    // if_there_is_still_data_in_the_queue_or_there_is_new_data_in_the_buffer，continue_playing
                    if (this.queue.length > 0) {
                        setTimeout(() => this.startPlaying(), 10);
                    } else if (audioBufferQueue.length > 0) {
                        // there_is_new_data_in_the_buffer，decode
                        const frames = [...audioBufferQueue];
                        audioBufferQueue = [];
                        this.decodeOpusFrames(frames);
                    } else if (this.endOfStream) {
                        // the_stream_has_ended_and_there_is_no_more_data
                        console.log("Audio playback completed");
                        isAudioPlaying = false;
                        streamingContext = null;
                    } else {
                        // waiting_for_more_data
                        setTimeout(() => {
                            // if_there_is_still_no_new_data，but_more_packages_arrive
                            if (this.queue.length === 0 && audioBufferQueue.length > 0) {
                                const frames = [...audioBufferQueue];
                                audioBufferQueue = [];
                                this.decodeOpusFrames(frames);
                            } else if (this.queue.length === 0 && audioBufferQueue.length === 0) {
                                // theres_really_no_more_data
                                console.log("Audio playback completed (timeout)");
                                isAudioPlaying = false;
                                streamingContext = null;
                            }
                        }, 500); // 500ms timeout
                    }
                };
                
                this.source.start();
            }
        };
    }
    
    // start_processing_buffered_data
    const frames = [...audioBufferQueue];
    audioBufferQueue = []; // clear_buffer_queue
    
    // decode_and_play
    streamingContext.decodeOpusFrames(frames);
}

// keep_the_old_playopusfromserver_function_as_a_fallback_method
function playOpusFromServerOld(opusData) {
    if (!opusDecoder) {
        initOpus().then(success => {
            if (success) {
                decodeAndPlayOpusDataOld(opusData);
            } else {
                statusLabel.textContent = "Opus decoder initialization failed";
            }
        });
    } else {
        decodeAndPlayOpusDataOld(opusData);
    }
}

// old_decoding_and_playback_functions_as_fallback
function decodeAndPlayOpusDataOld(opusData) {
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

// update_the_playopusfromserver_function_to_the_promise_version
function playOpusFromServer(opusData) {
    // for_compatibility，we_add_opusdata_to_audiobufferqueue_and_trigger_playback
    if (Array.isArray(opusData) && opusData.length > 0) {
        for (const frame of opusData) {
            audioBufferQueue.push(frame);
        }
        
        // if_not_playing_and_buffering，start_process
        if (!isAudioBuffering && !isAudioPlaying) {
            startAudioBuffering();
        }
        
        return new Promise(resolve => {
            // we_dont_know_exactly_when_playback_is_complete，so_set_a_reasonable_timeout
            setTimeout(resolve, 1000); // It is considered processed after 1 second
        });
    } else {
        // if_not_an_array_or_empty，use_old_methods
        return new Promise(resolve => {
            playOpusFromServerOld(opusData);
            setTimeout(resolve, 1000);
        });
    }
}

// connect_to_websocket_server
function connectToServer() {
    let url = serverUrlInput.value || "ws://127.0.0.1:8000/xiaozhi/v1/";
    
    try {
        // check_url_format
        if (!url.startsWith('ws://') && !url.startsWith('wss://')) {
            console.error('URL格式错误，must_be_ws:// Or starting with wss://');
            updateStatus('URL格式错误，must_be_ws:// Or start with wss://', ​​'error');
            return;
        }

        // add_authentication_parameters
        let connUrl = new URL(url);
        connUrl.searchParams.append('device_id', 'web_test_device');
        connUrl.searchParams.append('device_mac', '00:11:22:33:44:55');

        console.log(`connecting: ${connUrl.toString()}`);
        updateStatus(`connecting: ${connUrl.toString()}`, 'info');
        
        websocket = new WebSocket(connUrl.toString());

        // set_the_type_of_binary_data_received_to_arraybuffer
        websocket.binaryType = 'arraybuffer';

        websocket.onopen = async () => {
            console.log(`connected_to_server: ${url}`);
            updateStatus(`connected_to_server: ${url}`, 'success');
            isConnected = true;

            // send_hello_message_after_successful_connection
            await sendHelloMessage();

            if(connectButton.id === "connectButton") {
                connectButton.textContent = '断开';
                // connectButton.onclick = disconnectFromServer;
                connectButton.removeEventListener("click", connectToServer);
                connectButton.addEventListener("click", disconnectFromServer);
            }
            
            if(messageInput.id === "messageInput") {
                messageInput.disabled = false;
            }
            
            if(sendTextButton.id === "sendTextButton") {
                sendTextButton.disabled = false;
            }
        };

        websocket.onclose = () => {
            console.log('已断开连接');
            updateStatus('已断开连接', 'info');
            isConnected = false;

            if(connectButton.id === "connectButton") {
                connectButton.textContent = '连接';
                // connectButton.onclick = connectToServer;
                connectButton.removeEventListener("click", disconnectFromServer);
                connectButton.addEventListener("click", connectToServer);
            }
            
            if(messageInput.id === "messageInput") {
                messageInput.disabled = true;
            }
            
            if(sendTextButton.id === "sendTextButton") {
                sendTextButton.disabled = true;
            }
        };

        websocket.onerror = (error) => {
            console.error(`WebSocket错误:`, error);
            updateStatus(`WebSocket错误`, 'error');
        };

        websocket.onmessage = function (event) {
            try {
                // check_if_it_is_a_text_message
                if (typeof event.data === 'string') {
                    const message = JSON.parse(event.data);
                    handleTextMessage(message);
                } else {
                    // process_binary_data
                    handleBinaryMessage(event.data);
                }
            } catch (error) {
                console.error(`WebSocket消息处理错误:`, error);
                // nonjson_format_text_messages_are_displayed_directly
                if (typeof event.data === 'string') {
                    addMessage(event.data);
                }
            }
        };

        updateStatus('正在连接...', 'info');
    } catch (error) {
        console.error(`connection_error:`, error);
        updateStatus(`connection_failed: ${error.message}`, 'error');
    }
}

// disconnect_websocket
function disconnectFromServer() {
    if (!websocket) return;

    websocket.close();
    if (isRecording) {
        stopRecording();
    }
}

// send_hello_handshake_message
async function sendHelloMessage() {
    if (!websocket || websocket.readyState !== WebSocket.OPEN) return;

    try {
        // set_device_information
        const helloMessage = {
            type: 'hello',
            device_id: 'web_test_device',
            device_name: 'Web测试设备',
            device_mac: '00:11:22:33:44:55',
            token: 'your-token1' // The token configured in use_config.yaml
        };

        console.log('发送hello握手消息');
        websocket.send(JSON.stringify(helloMessage));

        // wait_for_server_response
        return new Promise(resolve => {
            // 5 seconds timeout
            const timeout = setTimeout(() => {
                console.error('等待hello响应超时');
                resolve(false);
            }, 5000);

            // temporarily_listen_to_messages_once，receive_hello_response
            const onMessageHandler = (event) => {
                try {
                    const response = JSON.parse(event.data);
                    if (response.type === 'hello' && response.session_id) {
                        console.log(`server_handshake_successful，session_id: ${response.session_id}`);
                        clearTimeout(timeout);
                        websocket.removeEventListener('message', onMessageHandler);
                        resolve(true);
                    }
                } catch (e) {
                    // ignore_nonjson_messages
                }
            };

            websocket.addEventListener('message', onMessageHandler);
        });
    } catch (error) {
        console.error(`send_hello_message_error:`, error);
        return false;
    }
}

// send_text_message
function sendTextMessage() {
    const message = messageInput ? messageInput.value.trim() : "";
    if (message === '' || !websocket || websocket.readyState !== WebSocket.OPEN) return;

    try {
        // send_listen_message
        const listenMessage = {
            type: 'listen',
            mode: 'manual',
            state: 'detect',
            text: message
        };

        websocket.send(JSON.stringify(listenMessage));
        addMessage(message, true);
        console.log(`send_text_message: ${message}`);

        if (messageInput) {
            messageInput.value = '';
        }
    } catch (error) {
        console.error(`send_message_error:`, error);
    }
}

// add_message_to_conversation_record
function addMessage(text, isUser = false) {
    if (!conversationDiv) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'server'}`;
    messageDiv.textContent = text;
    conversationDiv.appendChild(messageDiv);
    conversationDiv.scrollTop = conversationDiv.scrollHeight;
}

// update_status_information
function updateStatus(message, type = 'info') {
    console.log(`[${type}] ${message}`);
    if (statusLabel) {
        statusLabel.textContent = message;
    }
    if (connectionStatus) {
        connectionStatus.textContent = message;
        switch(type) {
            case 'success':
                connectionStatus.style.color = 'green';
                break;
            case 'error':
                connectionStatus.style.color = 'red';
                break;
            case 'info':
            default:
                connectionStatus.style.color = 'black';
                break;
        }
    }
}

// process_text_messages
function handleTextMessage(message) {
    if (message.type === 'hello') {
        console.log(`server_response：${JSON.stringify(message, null, 2)}`);
    } else if (message.type === 'tts') {
        // TTS status message
        if (message.state === 'start') {
            console.log('服务器开始发送语音');
        } else if (message.state === 'sentence_start') {
            console.log(`server_sends_voice_segment: ${message.text}`);
            // add_text_to_session_transcript
            if (message.text) {
                addMessage(message.text);
            }
        } else if (message.state === 'sentence_end') {
            console.log(`end_of_speech_segment: ${message.text}`);
        } else if (message.state === 'stop') {
            console.log('服务器语音传输结束');
        }
    } else if (message.type === 'audio') {
        // audio_control_messages
        console.log(`audio_control_message_received: ${JSON.stringify(message)}`);
    } else if (message.type === 'stt') {
        // voice_recognition_results
        console.log(`recognition_results: ${message.text}`);
        // add_recognition_results_to_session_records
        addMessage(`[speech_recognition] ${message.text}`, true);
    } else if (message.type === 'llm') {
        // big_model_reply
        console.log(`big_model_reply: ${message.text}`);
        // add_large_model_reply_to_session_record
        if (message.text && message.text !== '😊') {
            addMessage(message.text);
        }
    } else {
        // unknown_message_type
        console.log(`unknown_message_type: ${message.type}`);
        addMessage(JSON.stringify(message, null, 2));
    }
}

// send_voice_data_to_websocket
function sendOpusDataToServer(opusData) {
    if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        console.error('WebSocket未连接，无法发送音频数据');
        return false;
    }

    try {
        // send_binary_data
        websocket.send(opusData.buffer);
        console.log(`opus_audio_data_sent: ${opusData.length}byte`);
        return true;
    } catch (error) {
        console.error(`failed_to_send_audio_data:`, error);
        return false;
    }
}

// send_voice_start_and_end_signals
function sendVoiceControlMessage(state) {
    if (!websocket || websocket.readyState !== WebSocket.OPEN) return;

    try {
        const message = {
            type: 'listen',
            mode: 'manual',
            state: state  // 'start' or 'stop'
        };

        websocket.send(JSON.stringify(message));
        console.log(`send_voice${state === 'start' ? '开始' : '结束'}控制消息`);
    } catch (error) {
        console.error(`failed_to_send_voice_control_message:`, error);
    }
}
