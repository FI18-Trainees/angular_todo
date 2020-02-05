import { Priority } from 'src/enums/priority.enum';

export interface Todo {
    title: string;
    id: number;
    finished: boolean;
    list: string;
    priority: Priority;
    due_date?: Date;
    address?: string;
    description?: string;
    subtask?: string[];
    reminder?: Date;
}
