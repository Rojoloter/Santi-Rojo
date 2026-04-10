import {BaseChart} from "./BaseChart.tsx";
import {useMemo} from "react";

export type ChartProps = {
    label: string,
    data: number[],
    maxDataPoins: number,
    fill?: string,
    line?: string
}

export function Chart(props: ChartProps) {
    const preparedData = useMemo(() => {
        const points = props.data.map((point) => ({value: point * 100}));

        return [
            ...points,
            ...Array.from({length: props.maxDataPoins - points.length}).map(() => ({value: undefined}))
        ]
    }, [props.data, props.maxDataPoins]);
    return (
        <div className="chart-container">
            <h4 className="chart-label">{props.label}</h4>
            <BaseChart data={preparedData} fill={props.fill} line={props.line}/>
        </div>)
}