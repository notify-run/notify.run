import * as React from 'react';

interface CreateChannelStageProps {
    onCreateChannel: () => void;
    loading: boolean;
}

export class CreateChannelStage extends React.Component<CreateChannelStageProps, {}> {
    render() {
        return <div>
            <p>All notifications are sent to a <strong>channel</strong>, which is how
            notify.run knows how to route them. To get started, create a channel.
            </p>
            <button onClick={this.props.onCreateChannel} className="ui primary button">Create a Channel</button>
            {
                this.props.loading ? <div className="ui mini active inline loader"></div> : ''
            }
        </div>;
    }
}
