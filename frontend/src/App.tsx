import { configure } from 'mobx';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import "./App.scss";
import { MainView } from "./MainView";

declare let module: any;

window.oncontextmenu = function (event) {
	event.preventDefault();

	return false;
};
configure ({ enforceActions: "observed" });  // causes errors to be generated when modifying an observable outside of an action
console.log("ssoifdjsf")
ReactDOM.render(<MainView />, document.getElementById("root"));

if (module.hot) {
	module.hot.accept();
}
