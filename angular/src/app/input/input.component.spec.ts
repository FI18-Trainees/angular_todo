import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InputComponent } from './input.component';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule, MatInputModule, MatDatepickerModule, MatNativeDateModule } from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TodoService } from 'src/services/todo.service';
import { By } from '@angular/platform-browser';

describe('InputComponent', () => {
  let component: InputComponent;
  let fixture: ComponentFixture<InputComponent>;
  let todoService: TodoService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        MatFormFieldModule,
        BrowserAnimationsModule,
        MatInputModule,
        MatDatepickerModule,
        MatNativeDateModule,
      ],
      declarations: [ InputComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    todoService = TestBed.get(TodoService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('input values should be changeable, so inputs are working', () => {
    fixture.detectChanges();
    fixture.whenStable().then(() => {
      expect(true).toBeTruthy();
      const todoInput = fixture.debugElement.query(By.css('#todoInput'));
      const todoElement = todoInput.nativeElement;
      const dateInput = fixture.debugElement.query(By.css('#dateInput'));
      const dateElement = dateInput.nativeElement;

      expect(todoElement.value).toBe('');
      expect(dateElement.value).toBe('');

      todoElement.value = 'testValue';
      dateElement.value = '02/02/2020';

      expect(todoElement.value).toBe('testValue');
      expect(dateElement.value).toBe('02/02/2020');
    });
  });
});
