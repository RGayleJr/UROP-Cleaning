﻿import { observer } from "mobx-react";
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
        let commands = [ 
            "dcf.create_limiting_factor(df, 'PID', 'digits')",
            "dcf.change_value(df, 'PID', 1, 100002000)",
            "dcf.create_limiting_factor(df, 'ST_NAME', 'letters')",
            "dcf.make_titlecase(df, 'ST_NAME')",
            "dcf.change_nonenan_within_col(df, 'OWN_OCCUPIED', 'Unkown')"
        ];
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
            // <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
            <div className="main-container" >
                <div className="history">
                    <h2>History</h2>
                </div>
                <div className="toolbar">
                    <button className='toolbar-element btn-remove'>Remove</button>
                    <button className='toolbar-element btn-keep'>Keep</button>
                    <button className='toolbar-element btn-NoneNan'>None/Nan</button>
                    <button className='toolbar-element btn-createcol'>Create Col</button>
                    <div className='toolbar-element'>
                        <input type='text'placeholder= 'Search...' className='search-bar'></input>
                    </div>
                </div>
                <div className="table-container">
                    <DataTable rawData={this._csvRows} />
                </div>
                <button onClick={this.onCleanClick} className="btn-clean">Clean</button>
            </div>
        );
    }
}
