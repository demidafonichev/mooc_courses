import React from "react";
import ReactDOM from "react-dom";

import CourseCard from "./CourseCard";

import {baseUrl} from "./constants";

class CoursesCatalog extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            courses: []
        }

        this.searchCourses("");

        this.searchCourses = this.searchCourses.bind(this);
        this.searchCourseOnChangeHandler = this.searchCourseOnChangeHandler.bind(this);
    }

    searchCourses(searchText) {
        fetch(baseUrl + "courses/search_courses/",
            {
                method: "POST",
                body: JSON.stringify({"searchText": searchText})
            })
            .then(response => response.json())
            .then(responseJson => {
                this.setState({
                    courses: responseJson.courses
                })
            })
            .catch(error => console.log(error))
    }

    searchCourseOnChangeHandler(event) {
        let searchText = event.target.value;
        this.searchCourses(searchText);
    }

    render() {
        return (
            <div>
                <div className="row catalog-header">
                    <h1 className="col-lg-9 col-md-9 col-sm-6 my-4">Все курсы</h1>
                    <div className="search-panel col-lg-3 col-md-3 col-sm-6">
                        <input className="form-control"
                               placeholder="Поиск..."
                               onChange={this.searchCourseOnChangeHandler}/>
                    </div>
                </div>
                <div className="row">{
                    this.state.courses.map((course, index) => {
                        return <CourseCard key={"course" + index} course={course}/>;
                    })
                }</div>
                <a href={baseUrl + "courses/create_course/"}>
                    <button className="btn btn-dark">Создать курс</button>
                </a>
            </div>
        );
    }
}

ReactDOM.render(<CoursesCatalog/>, document.getElementById("coursesCatalog"))
