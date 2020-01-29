import { TestBed } from '@angular/core/testing';

import { TodoService } from './todo.service';
import { isObservable } from 'rxjs';

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

  it('#todoSub should return an observable of type Todo list', () => {
    expect(isObservable(todoService.todoSub)).toBeTruthy();
  });

  it('#getTodos with one pushed value should return Todo list with the pushed value', () => {
    todoService.addTodo('testValue');
    expect(todoService.getTodos).toEqual([{title: 'testValue'}]);
  });
});
