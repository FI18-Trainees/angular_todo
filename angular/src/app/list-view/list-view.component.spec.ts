import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatCardModule, MatCheckboxModule, MatDividerModule } from '@angular/material';

import { ListViewComponent } from './list-view.component';
import { Priority } from 'src/enums/priority.enum';
import { By } from '@angular/platform-browser';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('ListViewComponent', () => {
  let component: ListViewComponent;
  let fixture: ComponentFixture<ListViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatCardModule,
        MatCheckboxModule,
        MatDividerModule,
        HttpClientTestingModule
      ],
      declarations: [ ListViewComponent ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('test ng-for rendering of todo-lists', () => {
    component.openTodos = [{title: 'testOpenValue', id: 0, list: 'testList', priority: Priority.normal, finished: false}];
    component.finishedTodos = [{title: 'testFinishedValue', id: 1, list: 'testList', priority: Priority.normal, finished: false}];
    fixture.detectChanges();

    expect(fixture.debugElement.query(By.css('#openTitle')).nativeElement.innerHTML).toBe(component.openTodos[0].title);
    expect(fixture.debugElement.query(By.css('#finishedTitle')).nativeElement.innerHTML).toBe(component.finishedTodos[0].title);
  });

  it('check mat-checkbox for function', () => {
    component.openTodos = [{title: 'testOpenValue', id: 0, list: 'testList', priority: Priority.normal, finished: false}];
    component.finishedTodos = [{title: 'testFinishedValue', id: 1, list: 'testList', priority: Priority.normal, finished: false}];
    fixture.detectChanges();

    const openTodoElement = fixture.debugElement.query(By.css('#' + CSS.escape(component.openTodos[0].id.toString()))).nativeElement;
    // tslint:disable-next-line: max-line-length
    const finishedTodoElement = fixture.debugElement.query(By.css('#' + CSS.escape(component.finishedTodos[0].id.toString()))).nativeElement;

    fixture.detectChanges();

    expect(+openTodoElement.id).toBe(component.openTodos[0].id);
    expect(+finishedTodoElement.id).toBe(component.finishedTodos[0].id);
  });
});
