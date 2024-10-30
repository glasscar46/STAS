```mermaid
erDiagram
    Researcher {
        id
        name
    }

    Dataset {
        id
        name
    }

    Alphaset {
        id
        datasetId
    }

    T-Set {
        id
        datasetId
    }

    Model {
        id
        name
    }

    Annotation {
        id
        alphasetId
        tSetId
        annotationText
    }


```