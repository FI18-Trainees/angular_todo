import { TestBed } from '@angular/core/testing';

import { TodoService } from './todo.service';
import { Observable } from 'rxjs';
import { Todo } from 'src/interfaces/todo';

describe('TodoService', () => {
  let todoService: TodoService;
  beforeEach(() => {
    TestBed.configureTestingModule({});
    todoService = TestBed.get(TodoService);
  });

  it('should be created', () => {
    expect(todoService).toBeTruthy();
  });

  it('#getTodos without add should return empty Todo list', () => {
    expect(todoService.getTodos()).toEqual([]);
  });

  it('#getTodos with one pushed value should return Todo list with the pushed value', () => {
    todoService.addTodo('testValue');
    expect(todoService.getTodos).toEqual([{title: 'testValue'}]);
  });

  it('#todoSub should return an observable of type Todo list', () => {
    expect(todoService.todoSub).toBe(typeof(new Observable<Todo[]>()));
  });
});
