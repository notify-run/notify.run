import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { QuickStartFlow } from './quickstart/quickstart_flow';
import { ChannelPage } from './channel';

window.addEventListener('load', () => {
    let quickstartContainer = document.getElementById('quickstart');
    if (quickstartContainer) {
        ReactDOM.render(
            <QuickStartFlow />,
            quickstartContainer
        );
    }

    let match = document.location.pathname.match('/c/(.+)');
    if (match) {
        let channelId = match[1];
        let channelContainer = document.getElementById('channel');
        ReactDOM.render(
            <ChannelPage channelId={channelId} />,
            channelContainer
        );
    }
});
