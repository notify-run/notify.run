var webpack = require('webpack');
const path = require('path');

module.exports = {
    context: path.resolve('src'),
    entry: './main.tsx',
    output: {
        path: path.resolve('dist'),
        filename: 'main.js'
    },
    devtool: "source-map",
    plugins: [
        new webpack.EnvironmentPlugin([
            'NOTIFY_API_SERVER',
            'NOTIFY_WEB_SERVER',
        ]),
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