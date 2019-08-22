import React = require("react");
import { ValueConverter } from "./ValueConverter";
import { DataTableViewModel } from "./DataTableViewModel";
import { DataTableSelection } from "./DataTableSelection";
import { DataTableSelectionType } from "./DataTableSelectionType";

interface IProps {
    headers:string[];
    viewModel:DataTableViewModel
}

export class DataTableHeader extends React.Component<IProps> {
    props: any;

    constructor(props: any) {
        super(props)
    }

    render(): React.ReactNode {
        let cells = this.props.headers.map( (v:string, i:number) => <th className="datatable-cell head" key={i}>{v}</th>);
        return <tr onClick={()=>{console.log("header clicked");
            this.props.viewModel.Selections.push(new DataTableSelection(DataTableSelectionType.Column, 0));
            console.log(this.props.viewModel.Selections.length)}} className="datatable-row head">{cells}</tr>;
    }
}