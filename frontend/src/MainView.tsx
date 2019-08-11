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
    private  _selection: any[] = [];
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

    @action
    onRemoveClick = (e: React.MouseEvent) => {
        this._selection[0] = 'Remove';
        console.log('Remove');
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
                <div className="history">
                    <h2>History</h2>
                </div>
                <div className="toolbar">
                    <div className='first-sec'>
                        <button onClick={this.onRemoveClick} className='toolbar-element btn-remove'>Remove</button>
                        <button className='toolbar-element btn-keep'>Keep</button>
                        <button className='toolbar-element btn-NoneNan'>None/Nan</button>
                        <button className='toolbar-element btn-createcol'>Create Col</button>
                        <div className='toolbar-element'>
                            <input type='text'placeholder= 'Search...' className='search-bar'></input>
                            <input type='text' placeholder= 'Go to row...' className='go-to'></input>
                            <input type='text' placeholder= 'Go to col...' className='go-to'></input>
                        </div>
                    </div>
                    <div className='second-sec'>
                        <div className='gen-data'>Gen data goes here</div>
                        <div className='gen-data'>Pie graph, bar graph, etc...</div>
                        <div className='gen-data'>Changes depending on what's selected</div>
                    </div>
                    <div className='third-sec'>
                        <div className='specific-cmds'>Specific commands go here</div>
                        <div className='specific-cmds'>Also changes depending on selection</div>
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
