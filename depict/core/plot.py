class Plot:
    def __init__(self, make_figure, steps, description, figure, width,
                 grid_visible, width_session, session):
        self.make_figure = make_figure
        self.steps = steps
        self.description = description
        self.figure = figure
        self.width = width
        self.grid_visible = grid_visible
        self.width_session = width_session
        self.session = session

    def __add__(self, other):
        new_description = self.description + '<br>' + other.description
        fig_sum = self.make_figure()
        for step in self.steps + other.steps:
            step(fig_sum)
        return Plot(make_figure=self.make_figure,
                    steps=self.steps + other.steps,
                    description=new_description,
                    figure=fig_sum, width=self.width,
                    grid_visible=self.grid_visible,
                    width_session=self.width_session,
                    session=self.session)
