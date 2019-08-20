import { DataTableSelectionType } from "./DataTableSelectionType";

export class DataTableSelection {

    public Type:DataTableSelectionType;
    public Index:number;

    constructor(type:DataTableSelectionType, index:number) {
        this.Type = type;
        this.Index = index;
    }
}