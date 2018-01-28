import { NotifyAPI } from './api';
import { urlB64ToUint8Array } from './util';

export class SubscriptionManager {
    constructor(private pubKey: string) { }

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
            .then((pushSubscription) => {
                NotifyAPI.subscribe(channelId, pushSubscription);
            });
    }
}