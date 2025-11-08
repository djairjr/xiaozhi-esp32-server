import BlockingQueue from './utils/BlockingQueue.js';
import { log } from './utils/logger.js';

// audio_stream_playback_context_class
export class StreamingContext {
    constructor(opusDecoder, audioContext, sampleRate, channels, minAudioDuration) {
        this.opusDecoder = opusDecoder;
        this.audioContext = audioContext;

        // audio_parameters
        this.sampleRate = sampleRate;
        this.channels = channels;
        this.minAudioDuration = minAudioDuration;

        // initialize_queue_and_status
        this.queue = [];          // decoded_pcm_queue。now_playing
        this.activeQueue = new BlockingQueue(); // decoded_pcm_queue。ready_to_play
        this.pendingAudioBufferQueue = [];  // pending_cache_queue
        this.audioBufferQueue = new BlockingQueue();  // cache_queue
        this.playing = false;     // is_playing
        this.endOfStream = false; // whether_the_end_signal_is_received
        this.source = null;       // current_audio_source
        this.totalSamples = 0;    // the_total_number_of_samples_accumulated
        this.lastPlayTime = 0;    // last_played_timestamp
    }

    // cache_audio_array
    pushAudioBuffer(item) {
        this.audioBufferQueue.enqueue(...item);
    }

    // get_the_cache_queue_that_needs_to_be_processed，single_thread：there_will_be_no_security_issues_when_audiobufferqueue_is_always_updated
    async getPendingAudioBufferQueue() {
        // atomic_swap + clear
        [this.pendingAudioBufferQueue, this.audioBufferQueue] = [await this.audioBufferQueue.dequeue(), new BlockingQueue()];
    }

    // get_the_decoded_pcm_queue_that_is_being_played，single_thread：there_will_be_no_security_issues_when_activequeue_is_always_updated
    async getQueue(minSamples) {
        let TepArray = [];
        const num = minSamples - this.queue.length > 0 ? minSamples - this.queue.length : 1;
        // atomic_swap + clear
        [TepArray, this.activeQueue] = [await this.activeQueue.dequeue(num), new BlockingQueue()];
        this.queue.push(...TepArray);
    }

    // convert_int16_audio_data_to_float32_audio_data
    convertInt16ToFloat32(int16Data) {
        const float32Data = new Float32Array(int16Data.length);
        for (let i = 0; i < int16Data.length; i++) {
            // will[-32768,32767]the_range_is_converted_to[-1,1]
            float32Data[i] = int16Data[i] / (int16Data[i] < 0 ? 0x8000 : 0x7FFF);
        }
        return float32Data;
    }

    // decode_opus_data_to_pcm
    async decodeOpusFrames() {
        if (!this.opusDecoder) {
            log('Opus解码器未初始化，无法解码', 'error');
            return;
        } else {
            log('Opus解码器启动', 'info');
        }

        while (true) {
            let decodedSamples = [];
            for (const frame of this.pendingAudioBufferQueue) {
                try {
                    // decode_using_opus_decoder
                    const frameData = this.opusDecoder.decode(frame);
                    if (frameData && frameData.length > 0) {
                        // convert_to_float32
                        const floatData = this.convertInt16ToFloat32(frameData);
                        // use_a_loop_instead_of_the_spread_operator
                        for (let i = 0; i < floatData.length; i++) {
                            decodedSamples.push(floatData[i]);
                        }
                    }
                } catch (error) {
                    log("Opus decoding failed:" + error.message, 'error');
                }
            }

            if (decodedSamples.length > 0) {
                // use_a_loop_instead_of_the_spread_operator
                for (let i = 0; i < decodedSamples.length; i++) {
                    this.activeQueue.enqueue(decodedSamples[i]);
                }
                this.totalSamples += decodedSamples.length;
            } else {
                log('没有成功解码的样本', 'warning');
            }
            await this.getPendingAudioBufferQueue();
        }
    }

    // start_playing_audio
    async startPlaying() {
        while (true) {
            // if_at_least_0_is_accumulated.3 seconds of audio, start_playing
            const minSamples = this.sampleRate * this.minAudioDuration * 3;
            if (!this.playing && this.queue.length < minSamples) {
                await this.getQueue(minSamples);
            }
            this.playing = true;
            while (this.playing && this.queue.length) {
                // create_new_audio_buffer
                const minPlaySamples = Math.min(this.queue.length, this.sampleRate);
                const currentSamples = this.queue.splice(0, minPlaySamples);

                const audioBuffer = this.audioContext.createBuffer(this.channels, currentSamples.length, this.sampleRate);
                audioBuffer.copyToChannel(new Float32Array(currentSamples), 0);

                // create_audio_source
                this.source = this.audioContext.createBufferSource();
                this.source.buffer = audioBuffer;

                // create_gain_nodes_for_smooth_transitions
                const gainNode = this.audioContext.createGain();

                // apply_fade_effects_to_avoid_popping_sounds
                const fadeDuration = 0.02; // 20 milliseconds
                gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(1, this.audioContext.currentTime + fadeDuration);

                const duration = audioBuffer.duration;
                if (duration > fadeDuration * 2) {
                    gainNode.gain.setValueAtTime(1, this.audioContext.currentTime + duration - fadeDuration);
                    gainNode.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + duration);
                }

                // connect_the_node_and_start_playing
                this.source.connect(gainNode);
                gainNode.connect(this.audioContext.destination);

                this.lastPlayTime = this.audioContext.currentTime;
                log(`start_playing ${currentSamples.length} samples，about ${(currentSamples.length / this.sampleRate).toFixed(2)} second`, 'info');
                this.source.start();
            }
            await this.getQueue(minSamples);
        }
    }
}

// factory_function_to_create_streamingcontext_instances
export function createStreamingContext(opusDecoder, audioContext, sampleRate, channels, minAudioDuration) {
    return new StreamingContext(opusDecoder, audioContext, sampleRate, channels, minAudioDuration);
}