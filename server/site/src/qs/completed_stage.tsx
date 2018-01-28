import * as React from 'react';

interface CompletedStageProps {
    channelId: string;
}

export class CompletedStage extends React.Component<CompletedStageProps, {}> {
    render() {
        return <div>
            <p>
                <strong>Your channel is ready to be used!</strong>
            </p>
            <p>
                To send a message with <samp>curl</samp>, run the following command in a terminal:
            </p>
            <pre>$ curl https://notify.run/{this.props.channelId} -d "Hello World!"</pre>
            <p>
                If you have <samp>pip</samp>, you can also install and run the <samp>notify-run</samp> package
                and use the command-line interface:
            </p>
            <pre>{`$ pip install notify-run
$ notify-run -c https://notify.run/${this.props.channelId}
$ notify-run "Hello World!"`}</pre>
            <p>
                You can always
                visit <a style={{ fontWeight: 'bold' }} href={`https://notify.run/${this.props.channelId}`}>https://notify.run/{this.props.channelId}</a> to
                view a log of recent messages or subscribe new devices.
            </p>
        </div>;
    }
}
