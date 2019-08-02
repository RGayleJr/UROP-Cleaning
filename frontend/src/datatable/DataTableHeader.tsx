import React = require("react");
import { ValueConverter } from "./ValueConverter";

interface IProps {
    headers:string[];
}

export class DataTableHeader extends React.Component<IProps> {

    constructor(props: any) {
        super(props)
    }

    render(): React.ReactNode {
        let cells = this.props.headers.map( (v:string, i:number) => <th className="datatable-cell head" key={i}>{v}</th>);
        return <tr className="datatable-row head">{cells}</tr>;
    }
}