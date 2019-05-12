import * as React from 'react';
import { Config } from '../config';

interface CompletedStageProps {
    channelId: string;
}

export class CompletedStage extends React.Component<CompletedStageProps, {}> {
    render() {
        let channelLink = `${Config.WEB_SERVER}/c/${this.props.channelId}`;
        let channelEndpoint = `${Config.API_SERVER}/${this.props.channelId}`
        return <div>
            <p>
                <strong>Your channel is ready to be used!</strong>
            </p>
            <p>
                To send a message with <samp>curl</samp>, run the following command in a terminal:
            </p>
            <pre>$ curl {channelEndpoint} -d "Hello from notify.run"</pre>
            <p>
                If you have <samp>pip</samp>, you can also install and run the <samp>notify-run</samp> package
                and use the command-line interface:
            </p>
            <pre>{`$ pip install notify-run
$ notify-run configure ${channelEndpoint}
$ notify-run send "Hello from notify.run"`}</pre>
            <p>
                You can always
                visit <a style={{ fontWeight: 'bold' }} href={channelLink}>{channelLink}</a> to
                view a log of recent messages or subscribe new devices.
            </p>
        </div>;
    }
}
