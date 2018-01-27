import * as React from 'react';
import { NotifyAPI } from '../api';

export class Index extends React.Component {
    createChannel() {
        NotifyAPI.registerChannel().then((channelId) => {
            console.log(channelId);
            (this.props as any).history.push(`/c/${channelId}`);
        });
    }

    render() {
        return <div>
            <p><strong>notify.run</strong> lets you send notifications to your desktop or phone from the command line.</p>

            <p>To get started, <a href="#" onClick={this.createChannel.bind(this)}>create a channel</a>.</p>
        </div>
    }
}
