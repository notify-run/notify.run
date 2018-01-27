
export type Message = { channelId: string, message: string, time: string };

export namespace NotifyAPI {
    export const API_SERVER = process.env.NOTIFY_API_SERVER;

    function request(path: string, requestInit?: {}) {
        return fetch(API_SERVER + path, requestInit).then((c) => c.json());
    }

    export function registerChannel(): Promise<string> {
        return request('/api/register_channel', { method: 'POST' }).then((c) => c.channelId);
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

    export function getPubkey(): Promise<string> {
        return request('/api/pubkey').then((c) => c.pubKey);
    }

    export function getMessages(channelId: string): Promise<Message[]> {
        return request(`/${channelId}`);
    }
}