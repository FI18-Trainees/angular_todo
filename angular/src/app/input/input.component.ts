import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {

  inputValue;

  constructor() { }

  ngOnInit() {
  }

  handleInput(e: KeyboardEvent) {
    e.preventDefault();
    alert(this.inputValue);
    this.inputValue = '';
  }
}
