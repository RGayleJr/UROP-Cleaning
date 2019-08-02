import React = require("react");
import { DataTableHeader } from "./DataTableHeader";
import { DataTableRow } from "./DataTableRow";
import { StringValueConverter } from "./ValueConverter";
import { observer } from "mobx-react";
import "./DataTable.scss";

interface IProps {
    rawData?: string[],
    header?: string[],
    rows?: string[][],
}

@observer
export class DataTable extends React.Component<IProps> {

    constructor(props: any) {
        super(props);
    }

    render(): React.ReactNode {
        let headers, rows;
        if (this.props.rawData) {
            headers = this.props.rawData[0].split(",");
            rows = this.props.rawData.slice(1).map((rawRow, i) => <DataTableRow key={i} columns={rawRow.split(",")} converters={rawRow.split(",").map(r => new StringValueConverter())} />)
        }
        else {
            headers = this.props.header ? this.props.header : [];
            rows = this.props.rows ? this.props.rows : [];
            rows = rows.map((rawRow, i) => <DataTableRow key={i} columns={rawRow} converters={rawRow.map(r => new StringValueConverter())} />)
        }
        return <table className="datatable">
            <thead>
                <DataTableHeader headers={headers}></DataTableHeader>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>;
    }
}