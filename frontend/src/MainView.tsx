import { observer } from "mobx-react";
import * as React from "react";
import { DataTable } from "./datatable/DataTable";
import { observable, runInAction, action } from "mobx";
import { Gateway } from "./Gateway";
import "./MainView.scss"
import { DataTableViewModel } from "./datatable/DataTableViewModel";

@observer
export class MainView extends React.Component {
    @observable
    private _csvRows: string[];
    // private  _selection: any[] = [];
    // private _prev_click: string;
    private _dataTableViewModel:DataTableViewModel;
    constructor(props: any) {
        super(props);

        this._dataTableViewModel = new DataTableViewModel();
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
        // if (this._prev_click != Headers || this._prev_click != cells || this._prev_click != indices) {
        //     this._selection = [];
        // };
        console.log(this._dataTableViewModel)
        // this._selection.unshift('Remove');
        console.log('Remove');
        this._dataTableViewModel.Prev_Click = 'Remove';
        // if (this._dataTableViewModel.Selections.length > 0) {
        //     this._dataTableViewModel.Selections.forEach(element => {
        //         if (element in 
        //     });
        // }
        // if (this._selection != ['Remove',]) {
        //     let map_cmnds = [];
        //     for (var object of this._selection) {
        //         let temp = ['Remove',];
        //         if (object == 'Remove') {
        //             continue;
        //         };
        //         temp.push(object);
        //     };
        // };
    };

    @action
    onKeepClick = (e: React.MouseEvent) => {
        // this._selection.unshift('Keep');
        console.log(this._dataTableViewModel)
        console.log('Keep');
        this._dataTableViewModel.Prev_Click = 'Keep';
    //     if (this._selection != ['Keep',]) {
    //         let map_cmnds = [];
    //         for (var object of this._selection) {
    //             let temp = ['Remove',];
    //             if (object == 'Remove') {
    //                 continue;
    //             };
    //             temp.push(object);
    //         };
    //     };
    //     // add something that adds a confirm button to be clicked after selecting all the things to keep
    };

    @action
    // onTyping = (e: React.KeyboardEvent) ==> {
        
    // }

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
                    <DataTable viewModel={this._dataTableViewModel} rawData={this._csvRows} />
                </div>
                <button onClick={this.onCleanClick} className="btn-clean">Clean</button>
            </div>
        );
    }
}