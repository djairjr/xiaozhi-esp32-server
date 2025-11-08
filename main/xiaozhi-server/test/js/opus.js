import { log } from './utils/logger.js';
import { updateScriptStatus } from './document.js'


// check_if_the_opus_library_is_loaded
export function checkOpusLoaded() {
    try {
        // check_if_module_exists（global_variables_exported_by_local_libraries）
        if (typeof Module === 'undefined') {
            throw new Error('Opus库未加载，Module对象不存在');
        }

        // try_using_module_first.instance (the last line of export in libopus.js)
        if (typeof Module.instance !== 'undefined' && typeof Module.instance._opus_decoder_get_size === 'function') {
            // use_module.instance object replaces global Module object
            window.ModuleInstance = Module.instance;
            log('Opus库加载成功（use_module.instance）', 'success');
            updateScriptStatus('Opus库加载成功', 'success');

            // Hide status after 3 seconds
            const statusElement = document.getElementById('scriptStatus');
            if (statusElement) statusElement.style.display = 'none';
            return;
        }

        // if_there_is_no_module.instance，check_global_module_function
        if (typeof Module._opus_decoder_get_size === 'function') {
            window.ModuleInstance = Module;
            log('Opus库加载成功（使用全局Module）', 'success');
            updateScriptStatus('Opus库加载成功', 'success');

            // Hide status after 3 seconds
            const statusElement = document.getElementById('scriptStatus');
            if (statusElement) statusElement.style.display = 'none';
            return;
        }

        throw new Error('Opus解码函数未找到，可能Module结构不正确');
    } catch (err) {
        log(`Opus库加载失败，please_check_libopus.js文件是否存在且正确: ${err.message}`, 'error');
        updateScriptStatus('Opus库加载失败，please_check_libopus.js文件是否存在且正确', 'error');
    }
}


// create_an_opus_encoder
let opusEncoder = null;
export function initOpusEncoder() {
    try {
        if (opusEncoder) {
            return opusEncoder; // already_initialized
        }

        if (!window.ModuleInstance) {
            log('无法创建Opus编码器：ModuleInstance不可用', 'error');
            return;
        }

        // initialize_an_opus_encoder
        const mod = window.ModuleInstance;
        const sampleRate = 16000; // 16kHz sampling rate
        const channels = 1;       // mono
        const application = 2048; // OPUS_APPLICATION_VOIP = 2048

        // create_an_encoder
        opusEncoder = {
            channels: channels,
            sampleRate: sampleRate,
            frameSize: 960, // 60ms @ 16kHz = 60 * 16 = 960 samples
            maxPacketSize: 4000, // maximum_packet_size
            module: mod,

            // initialize_the_encoder
            init: function () {
                try {
                    // get_encoder_size
                    const encoderSize = mod._opus_encoder_get_size(this.channels);
                    log(`Opus编码器大小: ${encoderSize}byte`, 'info');

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
                        application
                    );

                    if (err < 0) {
                        throw new Error(`Opus编码器初始化失败: ${err}`);
                    }

                    // set_bitrate (16kbps)
                    mod._opus_encoder_ctl(this.encoderPtr, 4002, 16000); // OPUS_SET_BITRATE

                    // set_complexity (0-10, higher_quality_is_better_but_more_cpu_usage)
                    mod._opus_encoder_ctl(this.encoderPtr, 4010, 5);     // OPUS_SET_COMPLEXITY

                    // set_up_using_dtx (silence_frames_are_not_transmitted)
                    mod._opus_encoder_ctl(this.encoderPtr, 4016, 1);     // OPUS_SET_DTX

                    log("Opus encoder initialization successful", 'success');
                    return true;
                } catch (error) {
                    if (this.encoderPtr) {
                        mod._free(this.encoderPtr);
                        this.encoderPtr = null;
                    }
                    log(`Opus编码器初始化失败: ${error.message}`, 'error');
                    return false;
                }
            },

            // encode_pcm_data_to_opus
            encode: function (pcmData) {
                if (!this.encoderPtr) {
                    if (!this.init()) {
                        return null;
                    }
                }

                try {
                    const mod = this.module;

                    // allocate_memory_for_pcm_data
                    const pcmPtr = mod._malloc(pcmData.length * 2); // 2 bytes/int16

                    // copy_pcm_data_to_heap
                    for (let i = 0; i < pcmData.length; i++) {
                        mod.HEAP16[(pcmPtr >> 1) + i] = pcmData[i];
                    }

                    // allocate_memory_for_output
                    const outPtr = mod._malloc(this.maxPacketSize);

                    // encode
                    const encodedLen = mod._opus_encode(
                        this.encoderPtr,
                        pcmPtr,
                        this.frameSize,
                        outPtr,
                        this.maxPacketSize
                    );

                    if (encodedLen < 0) {
                        throw new Error(`Opus编码失败: ${encodedLen}`);
                    }

                    // copy_the_encoded_data
                    const opusData = new Uint8Array(encodedLen);
                    for (let i = 0; i < encodedLen; i++) {
                        opusData[i] = mod.HEAPU8[outPtr + i];
                    }

                    // free_memory
                    mod._free(pcmPtr);
                    mod._free(outPtr);

                    return opusData;
                } catch (error) {
                    log(`Opus编码出错: ${error.message}`, 'error');
                    return null;
                }
            },

            // destroy_the_encoder
            destroy: function () {
                if (this.encoderPtr) {
                    this.module._free(this.encoderPtr);
                    this.encoderPtr = null;
                }
            }
        };

        opusEncoder.init();
        return opusEncoder;
    } catch (error) {
        log(`failed_to_create_opus_encoder: ${error.message}`, 'error');
        return false;
    }
}