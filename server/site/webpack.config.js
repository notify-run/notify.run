var webpack = require('webpack');
const path = require('path');

module.exports = {
    context: path.resolve('src'),
    entry: './app.tsx',
    output: {
        path: path.resolve('dist'),
        filename: 'bundle.js'
    },
    devtool: "source-map",
    plugins: [
        new webpack.EnvironmentPlugin(['NOTIFY_API_SERVER']),
    ],
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json"]
    },
    module: {
        loaders: [
            { test: /\.[tj]sx?$/, loader: 'ts-loader', exclude: /node_modules/ },
        ]
    },
    devServer: {
        contentBase: path.join(__dirname, 'static'),
        historyApiFallback: {
            index: 'index.html'
        }
    }
}