import * as React from 'react';
import { NotifyAPI, ChannelResponse } from '../api';
import { CreateChannelStage } from './create_channel_stage';
import { SubscribeStage } from './subscribe_stage';
import { CompletedStage } from './completed_stage';

interface QuickStartFlowState {
    channelId?: string,
    pubKey?: string,
    channelReady: boolean,
    loading: boolean,
}

export class QuickStartFlow extends React.Component<{}, QuickStartFlowState> {
    constructor(props: {}) {
        super(props);

        this.state = {
            channelId: undefined,
            pubKey: undefined,
            channelReady: false,
            loading: false,
        };
    }

    createChannel() {
        this.setState({
            loading: true,
        });

        NotifyAPI.registerChannel().then((rcr: ChannelResponse) => {
            this.setState({
                loading: false,
                channelId: rcr.channelId,
                pubKey: rcr.pubKey,
            })
        });
    }

    channelReady() {
        this.setState({
            channelReady: true,
        });
    }

    render() {
        if (this.state.channelId === undefined || this.state.pubKey === undefined) {
            return <CreateChannelStage onCreateChannel={this.createChannel.bind(this)} loading={this.state.loading} />;
        } else if (!this.state.channelReady) {
            return <SubscribeStage
                pubKey={this.state.pubKey}
                channelId={this.state.channelId}
                onChannelReady={this.channelReady.bind(this)} />
        } else {
            return <CompletedStage channelId={this.state.channelId} />;
        }
    }
}