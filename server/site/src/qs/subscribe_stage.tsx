import * as React from 'react';

import { SubscriptionManager } from '../subscription';
import { Config } from '../config';

interface SubscribeStageProps {
    onChannelReady: () => void;
    channelId: string;
    pubKey: string;
}

interface SubscribeStageState {
    subscribed: boolean,
    supported: boolean,
    err?: Error,
}

export class SubscribeStage extends React.Component<SubscribeStageProps, SubscribeStageState> {
    subscriptionManager: SubscriptionManager;

    constructor(props: SubscribeStageProps) {
        super(props);

        this.subscriptionManager = new SubscriptionManager(this.props.pubKey);

        this.state = {
            subscribed: false,
            supported: this.subscriptionManager.checkBrowserSupport()
        };
    }

    onSubscribe() {
        this.subscriptionManager.subscribe(this.props.channelId).then(() => {
            this.setState({
                subscribed: true,
            })
        }).catch((e: Error) => {
            this.setState({
                err: e
            });
        });
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
                    {
                        this.state.supported ?
                            <p>Use the button below to subscribe on <em>this</em> device. To subscribe on
                                a <em>different</em> device, open the URL below or scan this QR code.
                                </p> :
                            <p>The device or browser you are using does not support the Web Push API, but you can
                                    receive notifications on another device by opening the URL below or scanning the
                                    QR code.
                                </p>
                    }

                    <pre>{Config.WEB_SERVER}/c/{this.props.channelId}</pre>
                    {
                        this.state.supported ? (
                            this.state.subscribed ?
                                <button onClick={this.onSubscribe.bind(this)}
                                    className="ui button disabled">Subscribed</button> :
                                <button onClick={this.onSubscribe.bind(this)}
                                    className="ui primary button">Subscribe on this device</button>
                        ) : ''
                    }

                    <button onClick={this.props.onChannelReady} className={'ui button' + (this.state.subscribed || !this.state.supported ? ' primary' : '')}>Continue</button>
                </div>
                <div className="seven wide column">
                    <embed type="image/svg+xml" src={`${Config.API_SERVER}/${this.props.channelId}/qr.svg`} />
                </div>
            </div>
            {
                this.state.err ?
                    <div className="ui negative message">
                        <div className="header">{this.state.err.name}</div>
                        <p>{this.state.err.message}</p>
                    </div> : ''
            }
        </div>;
    }
}
