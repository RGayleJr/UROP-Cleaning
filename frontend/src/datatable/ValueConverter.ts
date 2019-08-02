export abstract class ValueConverter {

    abstract Convert(input: string): string;
}

export class StringValueConverter extends ValueConverter {

    public Convert(input: string): string {
        return input;

    }
}

export class FloatValueConveter extends ValueConverter {

    private _precision: number = 2;

    constructor(precision: number) {
        super();
        this._precision = precision;
    }

    public Convert(input: string): string {
        return input;
    }
}

export class DateValueConveter extends ValueConverter {

    constructor() {
        super();
    }

    public Convert(input: string): string {
        let date = new Date(Date.parse(input));
        return date.getFullYear().toString();
    }
}