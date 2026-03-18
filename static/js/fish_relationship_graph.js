document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("fishRelationshipGraph");
  if (!container) return;

  const nodes = new vis.DataSet(
    JSON.parse(document.getElementById("graph-nodes").textContent)
  );

  const edges = new vis.DataSet(
    JSON.parse(document.getElementById("graph-edges").textContent)
  );

  const options = {
    nodes: {shape: "circle", size: 10, font: {face: "IBM Plex Sans", size: 13, color: "#FFFFFF", align: "middle"}},
    edges: {arrows: {to: {enabled: true, scaleFactor: 0.6 }}, font: {align: "middle", size: 10}, color: {color: "#5f8fa3"}},
    groups: {
    relation: {
        shape: "box", color: {background: "#00B69B", border: "#00B640"}, font: {size: 20}, margin: {top: 12, bottom: 12, left: 16, right: 16}
    },
    fish: {
        size: 40, color: { background: "#0077b6", border: "#001BB6" }, font: {size: 30, color: "#FFFFFF"}
    },
    habitat: {
        shape: "ellipse", color: { background: "#76B600", border: "#1BB600" }, font: {size: 18}, margin: {top: 12, bottom: 12, left: 16, right: 16}
    },
    alias: {
        shape: "box", color: {background: "#B6001B", border: "#f4a261"}, margin: {top: 12, bottom: 12, left: 16, right: 16}, font: {size: 20}
    },
    related_fish: {
        shape: "ellipse", color: {background: "#4000B6", border: "#001BB6"}, font: {size: 18}
    }},
    physics: {
        enabled: true,
        barnesHut: {
            gravitationalConstant: -1200,   
            centralGravity: 0.05,           
            springLength: 180,              
            springConstant: 0.01,           
            damping: 0.25,                  
            avoidOverlap: 0.5
        },
        stabilization: {
            enabled: false               
        }
    }
  };

  new vis.Network(container, { nodes, edges }, options);

});