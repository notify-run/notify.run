import * as React from 'react';

import { NotifyAPI, Message } from '../api';
import { SubscriptionManager } from '../subscription';

export class ChannelPage extends React.Component<any, any> {
    subscriptionManager: SubscriptionManager;

    constructor(props: any) {
        super(props);

        this.state = {
            channelId: props.match.params.channelId,
            messages: [],
        };
    }

    componentDidMount() {
        this.subscriptionManager = new SubscriptionManager();

        NotifyAPI.fetchMessages(this.state.channelId).then((messages) => {
            this.setState({ messages });
        })
    }

    enableNotify() {
        this.subscriptionManager.subscribe(this.state.channelId);
    }

    render() {
        return <div>
            <p>Channel: {this.state.channelId}</p>

            <p>To send the channel a message, run this command:</p>

            <p>curl {NotifyAPI.API_SERVER}/{this.state.channelId} -d "message goes here"</p>

            <p><a href="#" onClick={this.enableNotify.bind(this)}>enable notifications on this device</a></p>

            <embed type="image/svg+xml" src={NotifyAPI.getURLOfQR(this.state.channelId)} />

            <p>Messages:</p>

            {
                this.state.messages.map((message: Message, i: number) =>
                    <p key={i}>{message.time} {message.message}</p>
                )
            }
        </div>
    }
}
