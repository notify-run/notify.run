import * as React from 'react';
import * as moment from 'moment';

import { NotifyAPI, Message, ChannelResponse } from './api';
import { SubscriptionManager } from './subscription';
import { Config } from './config';


interface MessageListProps {
    messages: Message[],
}

class MessageList extends React.Component<MessageListProps, {}> {
    render() {
        if (this.props.messages.length == 0) {
            return <div><em>Messages to this channel will appear here.</em></div>;
        }

        return <div className="ui segment">
            <div className="ui feed">
                {
                    this.props.messages.map((message: Message, i: number) =>
                        <div className="event" key={i}>
                            <div className="content">
                                <div className="summary">
                                    <samp>{message.message}</samp>
                                    <div className="date">{message.time}</div>
                                </div>
                            </div>
                        </div>)
                }
            </div></div>;
    }
}


interface ChannelPageProps {
    channelId: string,
}

interface ChannelPageState {
    messages: Message[],
    loading: boolean,
}

export class ChannelPage extends React.Component<ChannelPageProps, ChannelPageState> {
    subscriptionManager: SubscriptionManager;

    constructor(props: any) {
        super(props);

        this.state = {
            messages: [],
            loading: true,
        };
    }

    loadChannel() {
        NotifyAPI.fetchChannel(this.props.channelId).then((response) => {
            this.subscriptionManager = new SubscriptionManager(response.pubKey);
            this.subscriptionManager.getSubscription().then((k) => {
                console.log(k);
            });

            this.setState({
                messages: response.messages || [],
                loading: false,
            });
        })
    }

    componentDidMount() {
        document.title = `channel ${this.props.channelId}`;

        this.loadChannel();

        setInterval(this.loadChannel.bind(this), 30 * 1000);
    }

    onSubscribe() {
        this.subscriptionManager.subscribe(this.props.channelId).then(() => {
            this.setState({
                //subscribed: true,
            })
        }).catch((e: Error) => {
            console.log(e);
        });
    }

    render() {
        if (this.state.loading) {
            return <div className="ui active centered inline loader"></div>;
        }

        let channelEndpoint = `${Config.API_SERVER}/${this.props.channelId}`
        return <div>
            <h2>Channel <samp>{this.props.channelId}</samp></h2>
            <h3>Recent messages</h3>
            <MessageList messages={this.state.messages} />

            <h3>Send Messages</h3>
            <p>To send the channel a message, run this command:</p>

            <pre>curl {channelEndpoint} -d "message goes here"</pre>


            <h3>Add Subscription</h3>

            <p><button onClick={this.onSubscribe.bind(this)}
                className="ui primary button">Subscribe on this device</button></p>

            <embed type="image/svg+xml" src={NotifyAPI.getURLOfQR(this.props.channelId)} />


        </div>
    }
}
