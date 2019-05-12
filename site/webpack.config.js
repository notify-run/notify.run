var webpack = require('webpack');
const path = require('path');

module.exports = {
    mode: 'production',
    context: path.resolve('src'),
    entry: './main.tsx',
    output: {
        path: path.resolve('dist'),
        filename: 'main.js'
    },
    devtool: "source-map",
    plugins: [
        new webpack.EnvironmentPlugin({
            'NOTIFY_API_SERVER': null,
            'NOTIFY_WEB_SERVER': null
        }),
    ],
    resolve: {
        extensions: [".ts", ".tsx", ".js", ".json"]
    },
    module: {
        rules: [
            {
                test: /\.[tj]sx?$/,
                loader: 'ts-loader',
                exclude: /node_modules/
            },
        ]
    },
    devServer: {
        contentBase: path.join(__dirname, 'static'),
        historyApiFallback: {
            index: '/channel.html'
        }
    }
}