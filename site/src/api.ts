import { Config } from './config';
import { Subscription } from './subscription';

export type Message = { channelId: string, message: string, time: string };
export type ChannelResponse = {
    channelId: string,
    pubKey: string,
    messages?: Message[],
    subscriptions: string[],
};

export namespace NotifyAPI {
    function request(path: string, requestInit?: {}) {
        return fetch(Config.API_SERVER + path, requestInit).then((c) => c.json());
    }

    export function registerChannel(): Promise<ChannelResponse> {
        return request('/api/register_channel', { method: 'POST' });
    }

    export function subscribe(channelId: string, subscription: Subscription): Promise<any> {
        let req = {
            method: 'POST',
            body: JSON.stringify(subscription),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }

        return request(`/${channelId}/subscribe`, req);
    }

    export function fetchChannel(channelId: string): Promise<ChannelResponse> {
        return request(`/${channelId}`);
    }

    export function getURLOfQR(channelId: string): string {
        return `${Config.API_SERVER}/${channelId}/qr.svg`;
    }
}