import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {
    BrowserRouter as Router,
    Route,
    Link
} from 'react-router-dom';

import { Index } from './pages/index';
import { ChannelPage } from './pages/channel';
import { NotifyAPI } from './api';

class App extends React.Component {
    render() {
        return <Router>
            <div>
                <Route exact path="/" component={Index} />
                <Route path="/c/:channelId" component={ChannelPage} />
            </div>
        </Router>;
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
);
