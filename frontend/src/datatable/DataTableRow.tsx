import React = require("react");
import { ValueConverter } from "./ValueConverter";
import { DataTableViewModel } from "./DataTableViewModel";

interface IProps {
    converters: ValueConverter[];
    columns: string[];
    viewModel:DataTableViewModel
}

export class DataTableRow extends React.Component<IProps> {
    props: any;

    constructor(props: any) {
        super(props)
    }

    render(): React.ReactNode {
        let cells = this.props.columns.map((v: string, i: number) => <td className="datatable-cell" key={i}>{this.props.converters[i].Convert(v)}</td>);
        return <tr onClick={()=>{console.log("row clicked")}} className="datatable-row">{cells}</tr>;
    }
}