import "./Roadmap.css";

import { useState } from "react";

import {
  Target,
  Rocket,
  BookOpen,
  Trophy
} from "lucide-react";

function Roadmap() {

  const [generated, setGenerated] =
    useState(false);

  return (

    <div className="roadmap-page">

      {!generated ? (

        <div className="roadmap-card">

          <Target size={70} />

          <h2>
            AI Roadmap Generator
          </h2>

          <p>
            Generate a learning roadmap
            for any career goal
          </p>

          <input
            type="text"
            placeholder="Goal (React Developer)"
          />

          <select>
            <option>
              3 Months
            </option>

            <option>
              6 Months
            </option>

            <option>
              12 Months
            </option>
          </select>

          <select>
            <option>
              Beginner
            </option>

            <option>
              Intermediate
            </option>

            <option>
              Advanced
            </option>
          </select>

          <button
            onClick={() =>
              setGenerated(true)
            }
          >
            Generate Roadmap
          </button>

        </div>

      ) : (

        <div className="roadmap-container">

          <div className="roadmap-header">

            <h2>
              React Developer Roadmap
            </h2>

            <button
              onClick={() =>
                setGenerated(false)
              }
            >
              Generate Again
            </button>

          </div>

          <div className="milestone-card">

            <BookOpen size={24} />

            <div>

              <h3>
                Month 1
              </h3>

              <p>
                HTML, CSS, JavaScript
              </p>

            </div>

            <div className="progress">
              100%
            </div>

          </div>

          <div className="milestone-card">

            <Rocket size={24} />

            <div>

              <h3>
                Month 2
              </h3>

              <p>
                React Basics & Components
              </p>

            </div>

            <div className="progress">
              75%
            </div>

          </div>

          <div className="milestone-card">

            <Trophy size={24} />

            <div>

              <h3>
                Month 3
              </h3>

              <p>
                APIs & Projects
              </p>

            </div>

            <div className="progress">
              40%
            </div>

          </div>

        </div>

      )}

    </div>

  );
}

export default Roadmap;