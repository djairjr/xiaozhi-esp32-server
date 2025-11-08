export default class BlockingQueue {
    #items   = [];
    #waiters = [];          // {resolve, reject, min, timer, onTimeout}

    /* empty_queue_oneshot_gate */
    #emptyPromise = null;
    #emptyResolve = null;

    /* producer：put_the_data_in */
    enqueue(item, ...restItems) {
        if (restItems.length === 0) {
            this.#items.push(item);
        }
        // if_there_are_additional_parameters，batch_all_items
        else {
            const items = [item, ...restItems].filter(i => i);
            if (items.length === 0) return;
            this.#items.push(...items);
        }
        // if_there_is_an_empty_queue_gate，release_all_waiters_at_once
        if (this.#emptyResolve) {
            this.#emptyResolve();
            this.#emptyResolve = null;
            this.#emptyPromise = null;
        }

        // wake_up_all_those_who_are_waiting waiter
        this.#wakeWaiters();
    }

    /* consumer：min article_or timeout ms who_comes_first */
    async dequeue(min = 1, timeout = Infinity, onTimeout = null) {
        // 1. if_empty，wait_for_the_first_data_to_arrive（all_calls_share_the_same promise）
        if (this.#items.length === 0) {
            await this.#waitForFirstItem();
        }

        // immediate_gratification
        if (this.#items.length >= min) {
            return this.#flush();
        }

        // need_to_wait
        return new Promise((resolve, reject) => {
            let timer = null;
            const waiter = { resolve, reject, min, onTimeout, timer };

            // timeout_logic
            if (Number.isFinite(timeout)) {
                waiter.timer = setTimeout(() => {
                    this.#removeWaiter(waiter);
                    if (onTimeout) onTimeout(this.#items.length);
                    resolve(this.#flush());
                }, timeout);
            }

            this.#waiters.push(waiter);
        });
    }

    /* empty_queue_gate_generator */
    #waitForFirstItem() {
        if (!this.#emptyPromise) {
            this.#emptyPromise = new Promise(r => (this.#emptyResolve = r));
        }
        return this.#emptyPromise;
    }

    /* internal：after_each_data_change，which_ones_to_check waiter satisfied */
    #wakeWaiters() {
        for (let i = this.#waiters.length - 1; i >= 0; i--) {
            const w = this.#waiters[i];
            if (this.#items.length >= w.min) {
                this.#removeWaiter(w);
                w.resolve(this.#flush());
            }
        }
    }

    #removeWaiter(waiter) {
        const idx = this.#waiters.indexOf(waiter);
        if (idx !== -1) {
            this.#waiters.splice(idx, 1);
            if (waiter.timer) clearTimeout(waiter.timer);
        }
    }

    #flush() {
        const snapshot = [...this.#items];
        this.#items.length = 0;
        return snapshot;
    }

    /* current_cache_length（does_not_include_waiters） */
    get length() {
        return this.#items.length;
    }
}