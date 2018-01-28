import { Config } from './config';

export type Message = { channelId: string, message: string, time: string };
export type RegisterChannelResponse = { channelId: string, pubKey: string };

export namespace NotifyAPI {
    function request(path: string, requestInit?: {}) {
        return fetch(Config.API_SERVER + path, requestInit).then((c) => c.json());
    }

    export function registerChannel(): Promise<RegisterChannelResponse> {
        return request('/api/register_channel', { method: 'POST' });
    }

    export function subscribe(channelId: string, subscription: any): Promise<any> {
        let req = {
            method: 'POST',
            body: JSON.stringify(subscription),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }

        return request(`/${channelId}/subscribe`, req);
    }

    export function fetchPubkey(): Promise<string> {
        return request('/api/pubkey').then((c) => c.pubKey);
    }

    export function fetchMessages(channelId: string): Promise<Message[]> {
        return request(`/${channelId}`);
    }

    export function getURLOfQR(channelId: string): string {
        return `${Config.API_SERVER}/${channelId}/qr.svg`;
    }
}