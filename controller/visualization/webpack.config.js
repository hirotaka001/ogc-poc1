const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = [
    {
        mode: 'production',
        entry: {
            app: [
                path.resolve(__dirname, 'static-src/js/cameraHeatmap.js'),
                path.resolve(__dirname, 'static-src/css/cameraHeatmap.scss')
            ],
        },
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
                                    ['env', {modules: false}]
                                ]
                            }
                        }
                    ]
                },
                {
                    test: /\.(scss|sass|css)$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader
                        },
                        {
                            loader: 'css-loader',
                            options: {
                                url: false,
                                importLoaders: 2
                            }
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                plugins: () => [
                                    require('cssnano')({preset: 'default'}),
                                    require('autoprefixer')({grid: true, browsers: ['> 1%', 'last 2 versions']})
                                ],
                            },
                        },
                        {
                            loader: 'sass-loader'
                        }
                    ]
                }
            ]
        },
        plugins: [
            new MiniCssExtractPlugin({filename: '../css/cameraHeatmap.css'})
        ],
        performance: {
            maxEntrypointSize: 512000,
            maxAssetSize: 512000
        }
    }
];
