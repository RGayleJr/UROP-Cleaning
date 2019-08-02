import React = require("react");
import { ValueConverter } from "./ValueConverter";

interface IProps {
    converters: ValueConverter[];
    columns: string[];
}

export class DataTableRow extends React.Component<IProps> {

    constructor(props: any) {
        super(props)
    }

    render(): React.ReactNode {
        let cells = this.props.columns.map((v: string, i: number) => <td className="datatable-cell" key={i}>{this.props.converters[i].Convert(v)}</td>);
        return <tr onClick={()=>{console.log("row clicked")}} className="datatable-row">{cells}</tr>;
    }
}