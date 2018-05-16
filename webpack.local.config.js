var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

var config = require('./webpack.base.config.js')
config.ip = 'localhost'

config.devtool = "#eval-source-map"

config.entry = {
  CoursesCatalog: [
    'webpack-dev-server/client?http://' + config.ip + ':3000',
    'webpack/hot/only-dev-server',
    './react/CoursesCatalog',
  ],
}

config.output.publicPath = 'http://' + config.ip + ':3000' + '/assets/bundles/'

config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new BundleTracker({filename: './webpack-stats-local.json'}),
])

config.module.loaders.push(
  { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel'] }
)

module.exports = config