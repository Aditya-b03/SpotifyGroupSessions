const path = require("path");
const webpack = require("webpack");


// Bundles all our javascript into one file
/*
The webpack configuration file webpack. config.
js is the file that contains all the configuration,
plugins, loaders, etc. to build the JavaScript part
of the NativeScript application. */
module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("development"),
      },
    }),
  ],
};