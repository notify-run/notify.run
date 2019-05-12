import { NotifyAPI } from './api';
import { urlB64ToUint8Array } from './util';

type Keys = { p256dh: string, auth: string };

export class Subscription {
    constructor(
        public id: string,
        public subscription: PushSubscription,
    ) { }

    static fromPushSubscriptionAsync(ps: PushSubscription): PromiseLike<Subscription> {
        let buf: Uint8Array = new (window as any).TextEncoder('utf-8').encode(ps.endpoint);
        return crypto.subtle.digest('SHA-1', buf).then((digest) => {
            let digArray = Array.from(new Uint8Array(digest));
            let digHex = digArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
            let keys = {
                auth: ps.getKey('auth'),
                p256dh: ps.getKey('p256dh'),
            }
            return new Subscription(digHex, ps);
        });
    }
}


export class SubscriptionManager {
    constructor(private pubKey: string) {

    }

    getSubscription(): Promise<Subscription> {
        if (typeof navigator.serviceWorker === 'undefined') {
            return new Promise((resolve, reject) => reject());
        }

        return navigator.serviceWorker.ready
            .then((serviceWorkerRegistration) =>
                serviceWorkerRegistration.pushManager.getSubscription()
            )
            .then(Subscription.fromPushSubscriptionAsync);
    }

    checkBrowserSupport(): boolean {
        return (('Notification' in window) &&
            ('serviceWorker' in navigator) &&
            ('PushManager' in window));
    }

    checkPermission(): boolean {
        return (Notification as any).permission !== 'denied';
    }

    subscribe(channelId: string): Promise<void> {
        return navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                const subscribeOptions = {
                    userVisibleOnly: true,
                    applicationServerKey: urlB64ToUint8Array(this.pubKey)
                };
                return registration.pushManager.subscribe(subscribeOptions);
            })
            .then(Subscription.fromPushSubscriptionAsync)
            .then((pushSubscription) => {
                NotifyAPI.subscribe(channelId, pushSubscription);
            });
    }
}