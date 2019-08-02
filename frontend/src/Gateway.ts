
export class Gateway {


    public static GetCleanCsv(commands: string[]): Promise<any> {
        return fetch("http://localhost:9050/cleaned", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(commands)
        });
    }

    public static GetOriginalCsv(): Promise<any> {
        return fetch("http://localhost:9050/original", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        });
    }
}
