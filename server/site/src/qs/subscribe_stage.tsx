import * as React from 'react';

import { SubscriptionManager } from '../subscription';

interface SubscribeStageProps {
    onChannelReady: () => void;
    channelId: string;
}

export class SubscribeStage extends React.Component<SubscribeStageProps, {}> {
    subscriptionManager: SubscriptionManager;

    constructor(props: SubscribeStageProps) {
        super(props);
        this.subscriptionManager = new SubscriptionManager();
    }

    render() {
        return <div>
            <div className="ui stackable grid">
                <div className="nine wide column">
                    <p>
                        Your new channel is called <samp style={{ fontWeight: 'bold' }}>{this.props.channelId}</samp>.
                    </p>
                    <p>
                        To recieve notifications on a device (such as a desktop or phone), <strong>subscribe</strong> them
                        to your channel. If multiple devices are subscribed to the same channel,
                        they will all receive notifications.
                    </p>
                    <p>
                        Use the button below to subscribe on <em>this</em> device. To subscribe on a <em>different</em> device, open the URL below
                        or scan this QR code.
                    </p>
                    <pre>https://notify.run/{this.props.channelId}</pre>
                    <button className="ui primary button">Subscribe on this device</button>
                    <button onClick={this.props.onChannelReady} className="ui button">Continue</button>
                </div>
                <div className="seven wide column">
                    <embed type="image/svg+xml" src={`https://notify.run/${this.props.channelId}/qr.svg`} />
                </div>
            </div>
        </div>;
    }
}
