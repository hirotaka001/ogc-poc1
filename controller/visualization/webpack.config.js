const path = require('path')

module.exports = {
    mode: 'production',
    entry: path.resolve(__dirname, 'js/cameraHeatmap.js'),
    output: {
        path: path.resolve(__dirname, 'static/js'),
        filename: 'cameraHeatmap.combined.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                ['env', {'modules': false}]
                            ]
                        }
                    }
                ]
            }
        ]
    }
};
