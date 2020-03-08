import { TestBed } from '@angular/core/testing';

import { TodoService } from './todo.service';
import { isObservable } from 'rxjs';
import { Todo } from 'src/interfaces/todo';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { map } from 'rxjs/operators';

describe('TodoService', () => {
  let todoService: TodoService;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ]
    });
    todoService = TestBed.get(TodoService);
  });

  it('should be created', () => {
    expect(todoService).toBeTruthy();
  });

  it('#getTodos without add should return an empty Todo list', () => {
    let todos: Todo[] = [];
    todoService.getTodos().pipe(
      map((result: Todo[]) => {
        todos = result;
      })
    );
    expect(todos).toEqual([]);
  });

  it('#todoSub should return an observable of type Todo list', () => {
    expect(isObservable<Todo[]>(todoService.todoSub())).toBeTruthy();
  });

  /*
  it('#getTodos.title should equal a before pushed title', () => {
    todoService.addTodo('testValue');
    const expectedResult: Todo[] = [{title: 'testValue', due_date: undefined, id: 0,
                                    finished: false, list: 'testList', priority: Priority.normal}];
    let result: Todo[] = [];
    todoService.getTodos().pipe(map((todos: Todo[]) => result = todos));
    expect(result[0].title === expectedResult[0].title).toBeTruthy();
  });

  it('#getTodos.due_date should equal a before pushed date', () => {
    const date: Date = new Date('01/31/2020');
    todoService.addTodo('testValue', date);
    const expectedResult: Todo[] = [{title: 'testValue', due_date: date, id: 0,
                                    finished: false, list: 'testList', priority: Priority.normal}];
    let result: Todo[] = [];
    todoService.getTodos().pipe(map((todos: Todo[]) => result = todos));
    expect(result[0].due_date === expectedResult[0].due_date).toBeTruthy();
  });

  it('#finishTodo should set property "finished" of todo to true', () => {
    const testTodo: Todo = {title: 'testValue', id: 0, priority: Priority.normal, list: 'testList',
                            finished: false};
    todoService.addTodo(testTodo.title);
    todoService.finishTodo(testTodo.id);
    let result: Todo[] = [];
    todoService.getTodos().pipe(map((todos: Todo[]) => result = todos));
    expect(result[0].finished).toBeTruthy();
  });
  */
});
