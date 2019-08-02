import { observer } from "mobx-react";
import * as React from "react";
import { DataTable } from "./datatable/DataTable";
import { observable, runInAction, action } from "mobx";
import { Gateway } from "./Gateway";
import "./MainView.scss"

@observer
export class MainView extends React.Component {
    @observable
    private _csvRows: string[];

    constructor(props: any) {
        super(props);
    }

    @action
    onCleanClick = (e: React.MouseEvent) => {
        let commands = [ "dcf.create_limiting_factor(df, 'PID', 'digits')", "dcf.keep_rows_with_nonenan_within_col(df, 'MOVE_IN_DATE')"];
        Gateway.GetCleanCsv(commands).then(response => {
            response.text().then(csvText => {
                runInAction(() => {
                    this._csvRows = csvText.split("\n");
                });
            });
        })
    };

    componentDidMount() {

        Gateway.GetOriginalCsv().then(response => {
            response.text().then(csvText => {
                runInAction(() => {
                    this._csvRows = csvText.split("\n");
                });
            });
        })
    }

    render() {
        return (
            <div className="main-container" >
                <DataTable rawData={this._csvRows} />
                <button onClick={this.onCleanClick} className="btn-clean">Clean</button>
            </div>
        );
    }
}
