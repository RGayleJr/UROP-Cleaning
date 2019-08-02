const path = require("path");
const publicPath = "";

const webpack = require("webpack")
const CopyWebpackPlugin = require("copy-webpack-plugin");
const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");
const TsconfigPathsPlugin = require('tsconfig-paths-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = env => {

  const outputDir = "build";
  let config = {
    entry: ["./src/App.tsx"],
    mode: "development",
    devtool: "source-map",
    output: {
      filename: "./bundle.js",
      path: path.resolve(__dirname, outputDir),
    },
    optimization: {
      removeAvailableModules: false,
      removeEmptyChunks: false,
      splitChunks: false
    },
    resolve: {
      extensions: [".js", ".jsx", ".json", ".ts", ".tsx"],
      mainFields: ['module', 'browser', 'main'],
      plugins: [new TsconfigPathsPlugin({ configFile: "tsconfig.json" })],
    },
    module: {
      rules: [
        {
          test: /\.(ts|tsx)$/,
          loader: "ts-loader",
          options: {
            transpileOnly: true,
            experimentalWatchApi: true,
          },
        },
        {
          test: /\.scss|css$/,
          use: [
            {
              loader: "style-loader" // creates style nodes from JS strings
            },
            {
              loader: "css-loader" // translates CSS into CommonJS
            },
            {
              loader: "sass-loader" // compiles Sass to CSS
            }
          ]
        }
      ]
    },
    plugins: [
      new CopyWebpackPlugin([{ from: "deploy", to: path.join(__dirname, outputDir) }]),
      new ForkTsCheckerWebpackPlugin(),
      new webpack.HotModuleReplacementPlugin()
    ]
  }

  config.devServer = {
    compress: false,
    host: "localhost",
    port: 1001,
    https: false,
    hot: false,
    watchContentBase: true,
    overlay: {
      warnings: true,
      errors: true
    }
  }
  
  return config;
};