import React from "react";

import {baseUrl} from "./constants";

export default class CourseCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = props.course;
    }

    render() {
        return (
            <div className="col-lg-3 col-md-4 col-sm-6 portfolio-item">
                <div className="card h-100">
                    <a href={baseUrl + "courses/get_course/" + this.state.id}>
                        <img className="card-img-top" src={this.state.cover} alt=""/>
                    </a>
                    <div className="card-body">
                        <h4 className="card-title">{this.state.title}</h4>
                        <p className="card-text">{this.state.description}</p>
                    </div>
                </div>
            </div>
        );
    }
}